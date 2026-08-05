"""Relay document changes between connected editors over Google Cloud Pub/Sub.

The module opens one Pub/Sub topic per document and one subscription per
document-and-user pair. `CollaborationService` below holds the whole implementation.

The `settings` import at L29 does not resolve. `app/core/config.py` defines a
`Settings` class and a `get_settings()` factory, and never creates a module-level
`settings` instance, so the import raises ImportError. The four
`settings.PROJECT_ID` reads, at L107, L108, L170 and L204, name a field absent from
that module's nine declared fields.

`asyncio` at L134 and `json` at L207 are never imported. Both uses sit inside
function bodies, so each raises NameError at first call rather than at import, and
neither name appears in the import block below.

Two imports go unused: `WebSocketDisconnect` at L26 and `Document` at L28.

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
    interpolate `settings.PROJECT_ID`.

    Public methods:
        connect: Register a socket and subscribe it to a document topic.
        disconnect: Drop a socket and delete its subscription.
        broadcast_change: Publish one change payload to a document topic.

    All three methods declare `async def` and contain no `await` expression. The
    Pub/Sub client calls inside them run synchronously, and each method waits on its
    future by blocking, at L139 and L208.
    """
    def __init__(self):
        """Build the Pub/Sub clients and the in-process connection registry.

        L65 builds a `PublisherClient` and L66 builds a `SubscriberClient`, so
        creating this service opens both Google Cloud clients before any caller
        connects. L67 sets `active_connections` to an empty dictionary.

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

        When subscription creation fails, L114 prints and L115 returns, so the
        socket registered at L104 keeps its place in `active_connections` with no
        subscription behind it. L139 blocks inside an `async def`, which stalls the
        event loop for the lifetime of the subscription.

        Args:
            websocket: Socket to register under this document and user.
            document_id: Document identifier. Names the Pub/Sub topic and keys the
                outer `active_connections` dictionary.
            user_id: Identifier of the connecting user. Keys the inner dictionary
                and forms the second part of the subscription name.

        Returns:
            None.

        Side effects:
            L104 registers the socket in `active_connections`. L107 derives the
            topic name and L108 the subscription name. L111 creates the Pub/Sub
            subscription. L136 subscribes the nested `callback`. L139 blocks on
            `future.result()`.

        Raises:
            Nothing. L112 and L140 catch every exception, and L114 and L142 print
            it.
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

            L133 calls `message.ack()` before L134 sends, so a delivery that fails
            has already been acknowledged and cannot be redelivered. L134 calls
            `asyncio.run`, and this module never imports `asyncio`, so the first
            message delivered raises NameError.

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
            L165 removes the socket from `active_connections`. L167 removes the
            document key once the inner dictionary is empty. L172 deletes the
            per-user Pub/Sub subscription named at L170.

        Raises:
            Nothing. L173 catches every exception and L175 prints it.
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

        L207 calls `json.dumps`, and this module never imports `json`, so the first
        call raises NameError.

        Args:
            document_id: Document identifier, interpolated into the topic name at
                L204.
            change: Change payload. L207 serializes the dictionary to JavaScript
                Object Notation (JSON) and encodes the result as UTF-8.

        Returns:
            None.

        Side effects:
            L204 derives the topic name. L207 publishes the encoded payload to the
            per-document topic. L208 waits on the publish future.

        Raises:
            Nothing. L209 catches every exception and L211 prints it.
        """
        topic_name = f"projects/{settings.PROJECT_ID}/topics/{document_id}"
        
        try:
            future = self.publisher.publish(topic_name, data=json.dumps(change).encode('utf-8'))
            future.result()
        except Exception as e:
            # Handle publishing error
            print(f"Error publishing change: {e}")