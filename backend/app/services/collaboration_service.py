"""Relay document changes between connected editors over Google Cloud Pub/Sub.

The module builds one Pub/Sub topic path per document and creates one subscription
per document-and-user pair. `CollaborationService` below holds the whole
implementation.

The module creates no topic. No `create_topic` call exists anywhere in this file
or in the repository. L20 and L60 interpolate a topic path into a string, and L24
passes that string to `create_subscription` as the `topic` argument. Only three
Pub/Sub operations run: `create_subscription` at L24, `subscribe` at L35 and
`delete_subscription` at L52, plus `publish` at L63. Every one of them requires
the topic to exist already, so L24 and L63 both fail against a project where
nothing else created it.

Authorization. The three public methods take `document_id` and `user_id` from the
caller and verify neither. No method checks a bearer token, compares the supplied
`user_id` against an authenticated identity, or tests whether that user may read
or write the named document. Whatever a caller passes decides which topic it
publishes to and which document stream it receives. No route constructs this
service, so no request path exercises it today, and any future route would have to
supply both checks itself.

Line references point at the pre-documentation layout of commit `06be74c`, so
they exclude docstrings added by this pass.

The `settings` import at L4 does not resolve. `app/core/config.py` defines a
`Settings` class and a `get_settings()` factory, and never creates a module-level
`settings` instance, so the import raises ImportError. The four
`settings.PROJECT_ID` reads, at L20, L21, L50 and L60, name a field absent from
that module's nine declared fields.

`asyncio` at L33 and `json` at L63 are never imported. Both uses sit inside
function bodies, so each raises NameError at first call rather than at import, and
neither name appears in the import block below.

Two imports go unused: `WebSocketDisconnect` at L1 and `Document` at L3.

No application module imports `CollaborationService`, and no WebSocket route exists
anywhere under `backend/`. The only references sit in
`backend/tests/test_services.py` at L4 and L39, which import through a bare
`services.*` root that does not resolve. The client uses a different transport:
`frontend/src/services/collaboration.ts:L1` imports `socket.io-client`, while
`connect` below declares a FastAPI `WebSocket`. The collaboration path is
unreachable.
"""
from fastapi import WebSocket, WebSocketDisconnect
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from app.schema.document import Document
from app.core.config import settings

class CollaborationService:
    """Register editor sockets and carry document changes through Pub/Sub.

    The class names one topic per document,
    `projects/{PROJECT_ID}/topics/{document_id}`, and one subscription per
    document-and-user pair,
    `projects/{PROJECT_ID}/subscriptions/{document_id}_{user_id}`. Both patterns
    interpolate `settings.PROJECT_ID`. Naming a topic is all the class does with
    one; no method creates a topic.

    No method authorizes its caller. Each takes identifiers as arguments and acts
    on them directly, so the trust decision belongs entirely to whatever code
    calls in.

    Public methods:
        connect: Register a socket and subscribe it to a document topic.
        disconnect: Drop a socket and delete its subscription.
        broadcast_change: Publish one change payload to a document topic.

    All three methods declare `async def` and contain no `await` expression. The
    Pub/Sub client calls inside them run synchronously, and each method waits on its
    future by blocking, at L38 and L64.
    """
    def __init__(self):
        """Build the Pub/Sub clients and the in-process connection registry.

        L8 builds a `PublisherClient` and L9 builds a `SubscriberClient`, so
        creating this service opens both Google Cloud clients before any caller
        connects. L10 sets `active_connections` to an empty dictionary.

        Attributes:
            publisher: Pub/Sub publisher client, used by `broadcast_change`.
            subscriber: Pub/Sub subscriber client, used by `connect` and
                `disconnect`.
            active_connections: Registry mapping a `document_id` to a dictionary
                that maps a `user_id` to a `WebSocket`. The registry is a plain
                per-process, unsynchronized dictionary, so a second worker process
                sees none of its contents.
        """
        self.publisher = PublisherClient()
        self.subscriber = SubscriberClient()
        self.active_connections = {}

    # HUMAN ASSISTANCE NEEDED
    # The following method has a confidence level of 0.6 and may need adjustments for production readiness
    async def connect(self, websocket: WebSocket, document_id: str, user_id: str) -> None:
        """Register a websocket and subscribe it to the document's topic.

        The comment block above this signature flags the method for
        production-readiness review.

        The method verifies nothing about its arguments. The method registers whatever
        socket it is handed under whatever `document_id` and `user_id` it is given,
        and subscribes that pair to the matching document stream, so any caller
        able to reach this method can receive another document's changes.

        When subscription creation fails, L27 prints and L28 returns, so the
        socket registered at L17 keeps its place in `active_connections` with no
        subscription behind it. L38 blocks inside an `async def`, which stalls the
        event loop for the lifetime of the subscription.

        A repeated document-and-user pair loses the earlier socket without closing
        it. L17 assigns into the registry unconditionally, so a second `connect`
        for the same pair overwrites the first entry before L24 runs. The `callback`
        that L31 defined during the first call closed over that first `websocket`
        parameter, and the streaming pull started at L35 still holds it, so
        messages keep arriving on the socket the registry no longer names. L24 then
        raises on the second call, because the subscription already exists, and L28
        returns after printing. The replacement socket therefore sits in the
        registry with no subscription of its own and receives nothing, while the
        displaced socket keeps receiving document updates.

        The streaming future is never retained. L35 binds `future` to a local
        name, L38 blocks on it, and nothing stores it on the instance, so no later
        call can cancel the pull. `disconnect` has no handle on it either.

        Args:
            websocket: Socket to register under this document and user.
            document_id: Document identifier. Names the Pub/Sub topic and keys the
                outer `active_connections` dictionary.
            user_id: Identifier of the connecting user. Keys the inner dictionary
                and forms the second part of the subscription name.

        Returns:
            None.

        Side effects:
            L17 registers the socket in `active_connections`. L20 derives the
            topic name and L21 the subscription name. L24 creates the Pub/Sub
            subscription. L35 subscribes the nested `callback`. L38 blocks on
            `future.result()`.

        Raises:
            Whatever `SubscriberClient.subscribe` raises at L35. That call sits
                between the two `try` blocks, outside both, so a synchronous
                client or argument-validation failure propagates to the caller. L23
                guards only `create_subscription` at L24, and L37 guards only
                `future.result()` at L38.
            NameError: From the nested `callback` at L33 on first delivery, as
                documented on that function. The error surfaces on the Pub/Sub
                client's own thread rather than through this method.
            Nothing else. L25 and L39 catch every exception their blocks raise,
                and L27 and L41 print it.
        """
        if document_id not in self.active_connections:
            self.active_connections[document_id] = {}
        self.active_connections[document_id][user_id] = websocket

        # Subscribe to document's Pub/Sub topic
        topic_name = f"projects/{settings.PROJECT_ID}/topics/{document_id}"
        subscription_name = f"projects/{settings.PROJECT_ID}/subscriptions/{document_id}_{user_id}"
        
        try:
            self.subscriber.create_subscription(name=subscription_name, topic=topic_name)
        except Exception as e:
            # Handle subscription creation error
            print(f"Error creating subscription: {e}")
            return

        # Handle incoming messages
        def callback(message):
            """Acknowledge one Pub/Sub message, then send its data to the socket.

            L32 calls `message.ack()` before L33 sends, so a delivery that fails
            has already been acknowledged and cannot be redelivered.

            Three separate defects sit on L33, and they surface in this order.
            First, `asyncio` is undefined, because the module never imports it, so
            the first message delivered raises NameError. Second, once that import
            exists, `message.data` is `bytes` on a Pub/Sub message, and
            `WebSocket.send_json` serializes its argument with `json.dumps`, which
            rejects `bytes`. Nothing decodes the payload, and
            `broadcast_change` at L63 encoded it as UTF-8 before publishing, so the
            round trip is unbalanced. Third, `asyncio.run` builds a new event loop
            and closes it on return, while the `WebSocket` belongs to the server's
            already-running loop. Driving a socket from a foreign loop fails, and
            `asyncio.run` refuses outright when a loop is already running on the
            calling thread.

            The Pub/Sub client invokes this function on its own thread, so an error
            here does not propagate to `connect`. The message stays acknowledged
            either way, because L32 ran first.

            Args:
                message: The delivered Pub/Sub message. The parameter carries no
                    type annotation.

            Returns:
                None. The signature declares no return type.
            """
            message.ack()
            asyncio.run(websocket.send_json(message.data))

        future = self.subscriber.subscribe(subscription_name, callback)
        
        try:
            future.result()
        except Exception as e:
            # Handle subscription error
            print(f"Subscription error: {e}")

    async def disconnect(self, document_id: str, user_id: str) -> None:
        """Drop a user's socket and delete the matching Pub/Sub subscription.

        Args:
            document_id: Document identifier. Keys the outer `active_connections`
                dictionary and forms the first part of the subscription name.
            user_id: Identifier of the departing user. Keys the inner dictionary and
                forms the second part of the subscription name.

        Returns:
            None.

        Side effects:
            L45 removes the socket from `active_connections`. L47 removes the
            document key once the inner dictionary is empty. L52 deletes the
            per-user Pub/Sub subscription named at L50.

        Raises:
            Nothing. L53 catches every exception and L55 prints it.

        The method verifies nothing about its arguments. Any caller able to reach
        it can drop another user's socket from the registry and delete that user's
        subscription, because L44 and L50 use the supplied identifiers directly.

        Three things the method does not clean up:

        - The socket itself. L45 removes the registry entry and no line calls
          `websocket.close()`, so the connection stays open on the client side with
          nothing on the server tracking it.
        - The streaming pull. `connect` never stored the future it created at L35,
          so this method has no handle to cancel. The pull keeps running and its
          `callback` keeps holding the socket it closed over.
        - The topic. L52 deletes only the per-user subscription. No `delete_topic`
          call exists, matching the absence of any `create_topic` call.

        Deleting the subscription stops new messages for that name, and messages
        Pub/Sub already delivered to the running pull are unaffected, so a socket
        displaced by the overwrite documented on `connect` can still receive
        document updates after its owner disconnects.
        """
        if document_id in self.active_connections and user_id in self.active_connections[document_id]:
            del self.active_connections[document_id][user_id]
            if not self.active_connections[document_id]:
                del self.active_connections[document_id]

        # Unsubscribe from document's Pub/Sub topic
        subscription_name = f"projects/{settings.PROJECT_ID}/subscriptions/{document_id}_{user_id}"
        try:
            self.subscriber.delete_subscription(subscription=subscription_name)
        except Exception as e:
            # Handle unsubscription error
            print(f"Error deleting subscription: {e}")

    # HUMAN ASSISTANCE NEEDED
    # The following method has a confidence level of 0.7 and may need adjustments for production readiness
    async def broadcast_change(self, document_id: str, change: dict) -> None:
        """Publish one change payload to the document's Pub/Sub topic.

        The comment block above this signature flags the method for
        production-readiness review.

        L63 calls `json.dumps`, and this module never imports `json`, so the first
        call raises NameError.

        The method verifies nothing about its arguments. The method publishes to
        the topic named for whatever `document_id` it receives. No check confirms
        that the caller may write to that document, and the method takes no user
        identifier. The payload reaches every subscriber of that document with no
        record of who sent it.

        The topic must already exist. L60 only builds a path string, and no method
        in this module creates a topic, so `publish` at L63 fails against a project
        where nothing else created it. The failure is silent to the caller: L65
        catches it and L67 prints.

        Args:
            document_id: Document identifier, interpolated into the topic name at
                L60.
            change: Change payload. L63 serializes the dictionary to JavaScript
                Object Notation (JSON) and encodes the result as UTF-8. The
                receiving `callback` at L31 does not decode it, as documented
                there.

        Returns:
            None.

        Side effects:
            L60 derives the topic name. L63 publishes the encoded payload to the
            per-document topic. L64 waits on the publish future.

        Raises:
            Nothing. L65 catches every exception and L67 prints it, so a caller
                cannot tell a delivered change from a dropped one.
        """
        topic_name = f"projects/{settings.PROJECT_ID}/topics/{document_id}"
        
        try:
            future = self.publisher.publish(topic_name, data=json.dumps(change).encode('utf-8'))
            future.result()
        except Exception as e:
            # Handle publishing error
            print(f"Error publishing change: {e}")