from typing import List, Dict, Any, Optional
import firebase_admin
from firebase_admin import credentials, messaging
from config.settings import settings
import logging
import time

logger = logging.getLogger(__name__)


class FirebaseNotificationManager:
    """
    Firebase notification manager for sending push notifications.
    Follows Single Responsibility Principle (SRP).
    """
    
    def __init__(self):
        self._app = None
        self._initialize_firebase()
    
    def _initialize_firebase(self) -> None:
        """Initialize Firebase app"""
        try:
            if settings.firebase_credentials_path and not firebase_admin._apps:
                cred = credentials.Certificate(settings.firebase_credentials_path)
                self._app = firebase_admin.initialize_app(cred)
                logger.info("Firebase initialized successfully")
            elif firebase_admin._apps:
                self._app = firebase_admin.get_app()
                logger.info("Using existing Firebase app")
            else:
                logger.warning("Firebase credentials not configured")
                
        except Exception as e:
            logger.error(f"Error initializing Firebase: {e}")
            self._app = None
    
    def send_notification(self, token: str, title: str, body: str, 
                         data: Optional[Dict[str, str]] = None) -> bool:
        """Send notification to a single device"""
        try:
            if not self._app:
                logger.warning("Firebase not initialized")
                return False
            
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data or {},
                token=token,
            )
            
            response = messaging.send(message)
            logger.info(f"Notification sent successfully: {response}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            return False
    
    def send_multicast_notification(self, tokens: List[str], title: str, body: str,
                                  data: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Send notification to multiple devices"""
        try:
            if not self._app:
                logger.warning("Firebase not initialized")
                return {"success_count": 0, "failure_count": len(tokens)}
            
            if not tokens:
                logger.warning("No tokens provided for multicast notification")
                return {"success_count": 0, "failure_count": 0}
            
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data or {},
                tokens=tokens,
            )
            
            response = messaging.send_multicast(message)
            
            logger.info(f"Multicast notification sent: {response.success_count} successful, {response.failure_count} failed")
            
            return {
                "success_count": response.success_count,
                "failure_count": response.failure_count,
                "responses": response.responses
            }
            
        except Exception as e:
            logger.error(f"Error sending multicast notification: {e}")
            return {"success_count": 0, "failure_count": len(tokens)}
    
    def send_topic_notification(self, topic: str, title: str, body: str,
                               data: Optional[Dict[str, str]] = None) -> bool:
        """Send notification to a topic"""
        try:
            if not self._app:
                logger.warning("Firebase not initialized")
                return False
            
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data or {},
                topic=topic,
            )
            
            response = messaging.send(message)
            logger.info(f"Topic notification sent successfully: {response}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending topic notification: {e}")
            return False
    
    def subscribe_to_topic(self, tokens: List[str], topic: str) -> Dict[str, Any]:
        """Subscribe tokens to a topic"""
        try:
            if not self._app:
                logger.warning("Firebase not initialized")
                return {"success_count": 0, "failure_count": len(tokens)}
            
            response = messaging.subscribe_to_topic(tokens, topic)
            
            logger.info(f"Topic subscription: {response.success_count} successful, {response.failure_count} failed")
            
            return {
                "success_count": response.success_count,
                "failure_count": response.failure_count
            }
            
        except Exception as e:
            logger.error(f"Error subscribing to topic: {e}")
            return {"success_count": 0, "failure_count": len(tokens)}
    
    def unsubscribe_from_topic(self, tokens: List[str], topic: str) -> Dict[str, Any]:
        """Unsubscribe tokens from a topic"""
        try:
            if not self._app:
                logger.warning("Firebase not initialized")
                return {"success_count": 0, "failure_count": len(tokens)}
            
            response = messaging.unsubscribe_from_topic(tokens, topic)
            
            logger.info(f"Topic unsubscription: {response.success_count} successful, {response.failure_count} failed")
            
            return {
                "success_count": response.success_count,
                "failure_count": response.failure_count
            }
            
        except Exception as e:
            logger.error(f"Error unsubscribing from topic: {e}")
            return {"success_count": 0, "failure_count": len(tokens)}


class NotificationService:
    """
    Notification service for handling application notifications.
    Follows Single Responsibility Principle (SRP) and Open/Closed Principle (OCP).
    """
    
    def __init__(self):
        self.firebase_manager = FirebaseNotificationManager()
    
    def send_new_post_notification(self, user_tokens: List[str], post_title: str, 
                                 author_name: str, post_id: str) -> Dict[str, Any]:
        """Send notification for new post"""
        try:
            title = "Nueva publicación"
            body = f"{author_name} ha publicado: {post_title}"
            data = {
                "type": "new_post",
                "post_id": post_id,
                "author": author_name
            }
            
            return self.firebase_manager.send_multicast_notification(user_tokens, title, body, data)
            
        except Exception as e:
            logger.error(f"Error sending new post notification: {e}")
            return {"success_count": 0, "failure_count": len(user_tokens)}
    
    def send_new_story_notification(self, user_tokens: List[str], author_name: str, 
                                  story_id: str) -> Dict[str, Any]:
        """Send notification for new story"""
        try:
            title = "Nueva historia"
            body = f"{author_name} ha publicado una nueva historia"
            data = {
                "type": "new_story",
                "story_id": story_id,
                "author": author_name
            }
            
            return self.firebase_manager.send_multicast_notification(user_tokens, title, body, data)
            
        except Exception as e:
            logger.error(f"Error sending new story notification: {e}")
            return {"success_count": 0, "failure_count": len(user_tokens)}
    
    def send_comment_notification(self, user_token: str, commenter_name: str, 
                                post_title: str, post_id: str) -> bool:
        """Send notification for new comment"""
        try:
            title = "Nuevo comentario"
            body = f"{commenter_name} ha comentado en tu publicación: {post_title}"
            data = {
                "type": "new_comment",
                "post_id": post_id,
                "commenter": commenter_name
            }
            
            return self.firebase_manager.send_notification(user_token, title, body, data)
            
        except Exception as e:
            logger.error(f"Error sending comment notification: {e}")
            return False
    
    def send_like_notification(self, user_token: str, liker_name: str, 
                             post_title: str, post_id: str) -> bool:
        """Send notification for new like"""
        try:
            title = "Le gusta tu publicación"
            body = f"A {liker_name} le gusta tu publicación: {post_title}"
            data = {
                "type": "new_like",
                "post_id": post_id,
                "liker": liker_name
            }
            
            return self.firebase_manager.send_notification(user_token, title, body, data)
            
        except Exception as e:
            logger.error(f"Error sending like notification: {e}")
            return False
    
    def send_event_notification(self, user_tokens: List[str], title: str, 
                              message: str) -> Dict[str, Any]:
        """Send general event notification"""
        try:
            data = {
                "type": "event",
                "timestamp": str(int(time.time()))
            }
            
            return self.firebase_manager.send_multicast_notification(user_tokens, title, message, data)
            
        except Exception as e:
            logger.error(f"Error sending event notification: {e}")
            return {"success_count": 0, "failure_count": len(user_tokens)}
    
    def subscribe_users_to_event(self, user_tokens: List[str], event_id: str) -> Dict[str, Any]:
        """Subscribe users to event topic"""
        try:
            topic = f"event_{event_id}"
            return self.firebase_manager.subscribe_to_topic(user_tokens, topic)
            
        except Exception as e:
            logger.error(f"Error subscribing users to event: {e}")
            return {"success_count": 0, "failure_count": len(user_tokens)}


# Singleton instance
notification_service = NotificationService() 