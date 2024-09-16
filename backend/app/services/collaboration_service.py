from fastapi import WebSocket, WebSocketDisconnect
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from app.schema.document import Document
from app.core.config import settings

class CollaborationService:
    def __init__(self):
        self.publisher = PublisherClient()
        self.subscriber = SubscriberClient()
        self.active_connections = {}

    # HUMAN ASSISTANCE NEEDED
    # The following method has a confidence level of 0.6 and may need adjustments for production readiness
    async def connect(self, websocket: WebSocket, document_id: str, user_id: str) -> None:
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
            message.ack()
            asyncio.run(websocket.send_json(message.data))

        future = self.subscriber.subscribe(subscription_name, callback)
        
        try:
            future.result()
        except Exception as e:
            # Handle subscription error
            print(f"Subscription error: {e}")

    async def disconnect(self, document_id: str, user_id: str) -> None:
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
        topic_name = f"projects/{settings.PROJECT_ID}/topics/{document_id}"
        
        try:
            future = self.publisher.publish(topic_name, data=json.dumps(change).encode('utf-8'))
            future.result()
        except Exception as e:
            # Handle publishing error
            print(f"Error publishing change: {e}")