from .auth_routes import router as auth_router
from .post_routes import router as post_router  
from .story_routes import router as story_router

__all__ = [
    "auth_router",
    "post_router",
    "story_router",
] 