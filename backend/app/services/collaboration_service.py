"""Relay document changes through Pub/Sub topic and subscription names.

The settings singleton, asyncio, and json references are unresolved.
No route constructs the service. The public methods also verify neither caller
identity nor document ownership.
Document and WebSocketDisconnect are imported but unused.
"""
from fastapi import WebSocket, WebSocketDisconnect
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from app.schema.document import Document
from app.core.config import settings

class CollaborationService:
    """Track per-document sockets and fan edits out through Pub/Sub.

    The service derives one Pub/Sub topic name per document and creates one
    subscription per document-user pair. The service does not create the topic.
`connect` and `broadcast_change` block on futures inside async methods.
`disconnect` makes a synchronous deletion call and waits on no future.

    Public methods:
        connect: Register a socket and subscribe it to a document's topic.
        disconnect: Drop a socket and delete its subscription.
        broadcast_change: Publish one change payload to a document's topic.

    Attributes:
        publisher: Pub/Sub publisher client.
        subscriber: Pub/Sub subscriber client.
        active_connections: Sockets held per document and per user for this
            process only, so a second worker process shares nothing.
    """

    def __init__(self):
        """Build both Pub/Sub clients and the in-process connection registry."""
        self.publisher = PublisherClient()
        self.subscriber = SubscriberClient()
        self.active_connections = {}

    # HUMAN ASSISTANCE NEEDED
    # The following method has a confidence level of 0.6 and may need adjustments for production readiness
    async def connect(self, websocket: WebSocket, document_id: str, user_id: str) -> None:
        """Register a socket for a document and subscribe it to the topic.

        See the assistance marker in the comment block directly above this
        signature. A failed subscription is printed and the method returns,
        which leaves the socket registered with no subscription behind it.

        Reconnecting the same document and user overwrites the registry entry.
        The first callback still closes over the old socket, and the streaming
        future is neither stored nor cancellable by `disconnect`.

        Args:
            websocket: The WebSocket to register for this document and user.
            document_id: Identifier of the document being edited.
            user_id: Identifier of the connecting user.

        Returns:
            Nothing, declared `None`.

        Raises:
            AttributeError: If settings.PROJECT_ID is unavailable.
            Exception: If subscriber.subscribe fails before future.result is
                guarded.

        Side effects:
            Adds the socket to `active_connections`, creates a Pub/Sub
            subscription, and then blocks on `future.result()`.
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

            Args:
                message: The Pub/Sub message delivered by the subscriber.

            Returns:
                Nothing.

            Raises:
                NameError: Because asyncio is not imported.
                TypeError: After that import is supplied, message.data is
                    bytes and send_json cannot encode it as JSON.
                RuntimeError: A server-owned WebSocket cannot safely run on
                    the new event loop created by asyncio.run.

            Side effects:
                Acknowledges the message before the forward is attempted, so a
                failed forward still consumes the message.
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
        """Drop a socket for a document and delete its subscription.

        Args:
            document_id: Identifier of the document being left.
            user_id: Identifier of the leaving user.

        Returns:
            Nothing, declared `None`.

        Raises:
            AttributeError: If settings.PROJECT_ID is unavailable. The read
                sits outside the guarded block, so the method does not catch
                the error.

        Side effects:
            Removes the user entry, removes the document entry once its last
            user leaves, and deletes the Pub/Sub subscription. The method
            closes neither socket nor streaming future, so displaced callbacks
            can retain stale delivery.
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
        """Publish one change payload to a document's Pub/Sub topic.

        See the assistance marker in the comment block directly above this
        signature. The method waits on the publish result, so the call blocks
        the event loop until Pub/Sub replies.

        Args:
            document_id: Identifier of the document that changed.
            change: The change payload to publish.

        Returns:
            Nothing, declared `None`.

        Raises:
            AttributeError: If settings.PROJECT_ID is unavailable. The read
                sits outside the guarded block, so the method does not catch
                the error.

        Side effects:
            Publishes one message and blocks on `future.result()`. The publish
            argument names the unresolved `json` module, so the surrounding
            `except Exception` catches the resulting NameError and prints it
            instead of delivering a message.
        """
        topic_name = f"projects/{settings.PROJECT_ID}/topics/{document_id}"
        
        try:
            future = self.publisher.publish(topic_name, data=json.dumps(change).encode('utf-8'))
            future.result()
        except Exception as e:
            # Handle publishing error
            print(f"Error publishing change: {e}")