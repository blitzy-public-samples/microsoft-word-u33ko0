"""Hold the collaboration service: socket registry plus Cloud Pub/Sub fan-out.

One Pub/Sub topic per document carries edits between editors. No module in the
tree imports this class and no WebSocket route exists, so nothing constructs
it and no edit ever reaches Pub/Sub.

Two modules are used and never imported: `asyncio` in the subscribe callback
and `json` in `broadcast_change`. Both raise `NameError` when first reached.
`settings.PROJECT_ID` is read three times and `app/core/config.py` declares
no such field, and `Document` is imported and never used.

The client half speaks Socket.IO in `frontend/src/services/collaboration.ts`,
while `connect` below declares a FastAPI `WebSocket`. See ./README.md.
"""
from fastapi import WebSocket, WebSocketDisconnect
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from app.schema.document import Document
from app.core.config import settings

class CollaborationService:
    """Track editor sockets per document and move edits over Pub/Sub.

    The registry is a plain dict on the instance, so it lives in one worker
    process. A second process holds its own registry and sees none of the
    first one's sockets.

    Public methods:
        connect: Register a socket and subscribe it to the document topic.
        disconnect: Remove a socket and delete its subscription.
        broadcast_change: Publish one change to the document topic.
    """
    def __init__(self):
        """Open the Pub/Sub clients and start with an empty registry.

        Both clients are built eagerly, so a missing credential fails at
        construction rather than at first publish.
        """
        self.publisher = PublisherClient()
        self.subscriber = SubscriberClient()
        self.active_connections = {}

    # HUMAN ASSISTANCE NEEDED
    # The following method has a confidence level of 0.6 and may need adjustments for production readiness
    async def connect(self, websocket: WebSocket, document_id: str, user_id: str) -> None:
        """Register an editor socket and subscribe it to the document topic.

        The socket is stored under the document and user identifiers, so a
        second socket for the same pair replaces the first at L66 without
        closing it, and the evicted editor stops receiving anything. Both
        connections resolve to one subscription name at L70, so the second
        `create_subscription` at L73 returns `AlreadyExists`, which L76
        prints before L77 returns, leaving that socket registered with no
        feed. A blocking `future.result()` then holds the coroutine open.
        See the HUMAN ASSISTANCE NEEDED marker above.

        Args:
            websocket: The connected client socket, a FastAPI `WebSocket`.
            document_id: Document the editor opened. Used as the topic name.
            user_id: The editing user, used in the subscription name.

        Returns:
            None. The body blocks until the subscription ends.
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
            """Acknowledge a Pub/Sub message and forward it to the socket.

            The message is acknowledged before the forward is attempted, so
            a failed send is not redelivered. `asyncio` is never imported,
            so the forward raises `NameError`, and the raw `message.data`
            bytes are handed to a method that expects a JSON-serialisable
            object.

            Args:
                message: The received Pub/Sub message.
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
        """Remove an editor socket and delete its Pub/Sub subscription.

        The document entry is dropped once its last socket goes at L121.
        L124 rebuilds the subscription name from the document and user
        alone, so L126 deletes the name every socket for that pair shares,
        and closing one tab cuts the feed to another. Deletion errors print.

        Args:
            document_id: Document the editor was working on.
            user_id: The editing user.

        Returns:
            None.
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
        """Publish one change to the document topic and wait for the result.

        The publish future is resolved inline, so the coroutine blocks until
        Pub/Sub acknowledges. `json` is never imported, so the encode below
        raises `NameError`. Failures are printed and swallowed, so a caller
        cannot tell a published change from a dropped one. See the HUMAN
        ASSISTANCE NEEDED marker above.

        Args:
            document_id: Document whose topic receives the change.
            change: The change payload, encoded as JSON bytes.

        Returns:
            None.
        """
        topic_name = f"projects/{settings.PROJECT_ID}/topics/{document_id}"
        
        try:
            future = self.publisher.publish(topic_name, data=json.dumps(change).encode('utf-8'))
            future.result()
        except Exception as e:
            # Handle publishing error
            print(f"Error publishing change: {e}")