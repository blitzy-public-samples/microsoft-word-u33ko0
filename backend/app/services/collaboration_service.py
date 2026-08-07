"""Fan document changes out to per-document Cloud Pub/Sub topics.

`settings` is requested from `app.core.config`, which never defines it, so importing
this module raises `ImportError`. `WebSocketDisconnect` and `Document` are imported and
unused. `asyncio` and `json` are used and never imported, so `connect` and
`broadcast_change` each raise `NameError` when they run.

The module creates no topic. No `create_topic` call exists anywhere in this file
or in the repository. L120 and L245 interpolate a topic path into a string, and L124
passes that string to `create_subscription` as the `topic` argument. Four Pub/Sub
calls run: `create_subscription` at L124, `subscribe` at L165, `delete_subscription`
at L211 and `publish` at L248. Two of the four name a topic and need it to exist
already, so L124 and L248 both fail against a project where nothing else created it.
The other two address a subscription instead: L165 consumes the subscription path
built at L121, and L211 deletes the subscription path built at L209.

Resilience. The module configures none, and every absence below belongs to this
module rather than to the client library. `PublisherClient()` at L69 and
`SubscriberClient()` at L70 receive no `client_options`, no publisher batch or flow
control settings and no credentials. The four operations pass no `retry` and no
`timeout` argument. `create_subscription` at L124 sets no `dead_letter_policy`, no
`ack_deadline_seconds`, no `retry_policy` and no `message_retention_duration`, so
no redelivery policy and no dead-letter route exists for a message the client
fails to handle. `future.result()` at L168 and L249 is called with no timeout, so
each call blocks indefinitely on a stalled future. No circuit breaker, no backoff,
no jitter and no fallback path exists. The `callback` at L131 acknowledges each
message at L162 before it attempts delivery at L163, so a delivery that fails
cannot be redelivered and the change it carried is lost. No backend dependency
manifest is committed, so nothing pins `google-cloud-pubsub` and no committed file
records which defaults the resolved release would apply.

No route constructs this class, so the whole path is unreachable. The client half speaks
Socket.IO while `connect` expects a FastAPI `WebSocket`, and no WebSocket route exists
to join them.
"""
from fastapi import WebSocket, WebSocketDisconnect
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from app.schema.document import Document
from app.core.config import settings

class CollaborationService:
    """Track live editor connections and bridge them to Pub/Sub.

    One publisher, one subscriber and one connection registry per instance. The registry
    is a plain dictionary in process memory, so a second server process shares none of
    it.

    No method authorizes its caller. Each takes identifiers as arguments and acts
    on them directly, so the trust decision belongs entirely to whatever code
    calls in.

    Public methods:
        connect: Register a socket and subscribe it to a document topic.
        disconnect: Drop a socket and delete its subscription.
        broadcast_change: Publish one change payload to a document topic.

    All three methods declare `async def` and contain no `await` expression, so the
    Pub/Sub client calls inside them run synchronously. Future handling differs by
    method, and only two of the three produce a future at all. `connect` binds the
    streaming pull future that `subscribe` returns at L165 and blocks on it at L168,
    which stalls the event loop for the lifetime of the subscription.
    `broadcast_change` binds the publish future that `publish` returns at L248 and
    blocks on it at L249. `disconnect` creates no future: L211 calls
    `delete_subscription`, which returns nothing to wait on, so the method has
    nothing to block for and nothing to cancel.
    """
    def __init__(self):
        """Open the Pub/Sub clients and start with an empty connection registry."""
        self.publisher = PublisherClient()
        self.subscriber = SubscriberClient()
        self.active_connections = {}

    # HUMAN ASSISTANCE NEEDED
    # The following method has a confidence level of 0.6 and may need adjustments for production readiness
    async def connect(self, websocket: WebSocket, document_id: str, user_id: str) -> None:
        """Register one editor connection and subscribe it to the document's topic.

        Args:
            websocket: Live connection to the editing client. Stored in the registry and
                written to from the subscription callback.
            document_id: Document being edited, used as both the topic name and the
                registry key.
            user_id: Editor identifier, used as the registry key within the document and
                as part of the subscription name.

        Returns:
            Nothing.

        Raises:
            AttributeError: At L120, because `Settings` declares no `PROJECT_ID`
                field. The read sits above the `try` at L123, outside every guarded
                block, so the error propagates to the caller on the first call.
                Partial state at that point: L117 has already registered the socket
                in `active_connections`, and no Pub/Sub call has run. The socket
                therefore sits in the registry with no subscription behind it, and
                the caller cannot tell from the exception that the registry was
                mutated.
            Whatever `SubscriberClient.subscribe` raises at L165. That call sits
                between the two `try` blocks, outside both, so a synchronous
                client or argument-validation failure propagates to the caller. L123
                guards only `create_subscription` at L124, and L167 guards only
                `future.result()` at L168.
            NameError: From the nested `callback` at L163 on first delivery, as
                documented on that function. The error surfaces on the Pub/Sub
                client's own thread rather than through this method.

        No other exception leaves the method. L125 and L169 catch every exception
        their own blocks raise, and L127 and L171 print it.

        Note:
            See the human-assistance marker at L73-L74 directly above this
            signature: the method carries a confidence level of 0.6 and is
            flagged for production-readiness adjustments.
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

            L162 calls `message.ack()` before L163 sends, so a delivery that fails
            has already been acknowledged and cannot be redelivered.

            Three separate defects sit on L163, and they surface in this order.
            First, `asyncio` is undefined, because the module never imports it, so
            the first message delivered raises NameError. Second, once that import
            exists, `message.data` is `bytes` on a Pub/Sub message, and
            `WebSocket.send_json` serializes its argument with `json.dumps`, which
            rejects `bytes`. Nothing decodes the payload, and
            `broadcast_change` at L248 encoded it as UTF-8 before publishing, so the
            round trip is unbalanced. Third, `asyncio.run` builds a new event loop
            and closes it on return, while the `WebSocket` belongs to the server's
            already-running loop. Driving a socket from a foreign loop fails, and
            `asyncio.run` refuses outright when a loop is already running on the
            calling thread.

            The Pub/Sub client invokes this function on its own thread, so an error
            here does not propagate to `connect`. The message stays acknowledged
            either way, because L162 ran first.

            Args:
                message: The delivered Pub/Sub message. The parameter carries no
                    type annotation.

            The two side effects are the acknowledgement at L162 and the socket send
            at L163. The signature declares no return annotation, and the Pub/Sub
            client discards the value the body evaluates to.
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
        """Drop one editor connection and delete its subscription.

        Args:
            document_id: Document the editor was working on.
            user_id: Editor identifier.

        Returns:
            Nothing.

        Raises:
            AttributeError: At L209, because `Settings` declares no `PROJECT_ID`
                field. The read sits above the `try` at L210, outside the guarded
                block, so the error propagates to the caller on the first call.
                Partial state at that point: L204 has already removed the socket
                from `active_connections`, and L206 has already removed the document
                key when that removal emptied the inner dictionary. L211 never runs,
                so the per-user Pub/Sub subscription survives while the registry
                entry that named it is gone, and no later call can find the pair to
                clean it up.

        No other exception leaves the method. L212 catches every exception the body
        raises and L214 prints it.

        Note:
            Removes the document's registry entry once its last editor leaves, so the
            registry does not grow without bound. Deletes the subscription synchronously
            and waits on no future. Logs a deletion failure and returns, so a caller
            cannot tell a clean disconnect from a leaked subscription.
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
        """Publish one change to the document's Pub/Sub topic.

        Args:
            document_id: Document the change belongs to, used as the topic name.
            change: Change payload, serialized to UTF-8 encoded JSON as the message
                body.

        Returns:
            Nothing.

        Raises:
            AttributeError: At L245, because `Settings` declares no `PROJECT_ID`
                field. The read sits above the `try` at L247, outside the guarded
                block, so the error propagates to the caller on the first call. No
                partial state follows: L245 is the method's first statement, no
                Pub/Sub call runs, and nothing is published.

        No other exception leaves the method. L250 catches every exception the body
        raises and L252 prints it, so a caller cannot tell a delivered change from a
        dropped one.

        Note:
            See the human-assistance marker at L216-L217 directly above this
            signature: the method carries a confidence level of 0.7 and is
            flagged for production-readiness adjustments.
        """
        topic_name = f"projects/{settings.PROJECT_ID}/topics/{document_id}"
        
        try:
            future = self.publisher.publish(topic_name, data=json.dumps(change).encode('utf-8'))
            future.result()
        except Exception as e:
            # Handle publishing error
            print(f"Error publishing change: {e}")