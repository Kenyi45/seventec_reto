from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time

# Import configurations and database
from config.settings import settings
from database.connection import db_connection

# Import routes
from routes import auth_router, post_router, story_router

# Import models for response formatting
from models.base import BaseResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting up App Convention API...")
    
    try:
        # Connect to database
        await db_connection.connect()
        logger.info("Database connection established")
        
        yield
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    
    finally:
        # Shutdown
        logger.info("Shutting down App Convention API...")
        
        try:
            # Disconnect from database
            await db_connection.disconnect()
            logger.info("Database connection closed")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    App Convention - Plataforma digital para gestionar eventos corporativos
    
    ## Características principales
    
    * **Autenticación JWT** - Sistema seguro de autenticación con roles
    * **Gestión de publicaciones** - Crear, leer, comentar y dar like a publicaciones  
    * **Historias temporales** - Contenido que se elimina automáticamente tras 24 horas
    * **Notificaciones push** - Notificaciones en tiempo real con Firebase Cloud Messaging
    * **Roles de usuario** - Organizadores pueden crear contenido, participantes pueden interactuar
    
    ## Roles
    
    * **Organizador**: Puede crear publicaciones e historias, acceso al panel administrador
    * **Participante**: Puede leer, comentar y dar like a publicaciones y historias
    """,
    lifespan=lifespan,
    debug=settings.debug,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom middleware for request logging and timing
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log requests and measure response time.
    """
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    try:
        response = await call_next(request)
        
        # Calculate response time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {response.status_code} - "
            f"Time: {process_time:.3f}s - "
            f"{request.method} {request.url}"
        )
        
        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
        
    except Exception as e:
        # Log error
        process_time = time.time() - start_time
        logger.error(
            f"Error: {str(e)} - "
            f"Time: {process_time:.3f}s - "
            f"{request.method} {request.url}"
        )
        raise


# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Global HTTP exception handler.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse(
            success=False,
            message=exc.detail,
            errors={"detail": exc.detail}
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Global general exception handler.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=BaseResponse(
            success=False,
            message="Error interno del servidor",
            errors={"detail": "Internal server error"}
        ).dict()
    )


# Include routes
app.include_router(auth_router, prefix="/api/v1")
app.include_router(post_router, prefix="/api/v1")
app.include_router(story_router, prefix="/api/v1")


# Health check endpoint
@app.get("/health", response_model=BaseResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the application and its dependencies.
    """
    try:
        # Check database connection
        db_healthy = await db_connection.health_check()
        
        health_status = {
            "status": "healthy" if db_healthy else "unhealthy",
            "database": "connected" if db_healthy else "disconnected",
            "version": settings.app_version,
            "timestamp": time.time()
        }
        
        return BaseResponse(
            success=db_healthy,
            message="Health check completed",
            data=health_status
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return BaseResponse(
            success=False,
            message="Health check failed",
            errors={"detail": str(e)}
        )


# Root endpoint
@app.get("/", response_model=BaseResponse, tags=["root"])
async def root():
    """
    Root endpoint with API information.
    """
    return BaseResponse(
        success=True,
        message="App Convention API",
        data={
            "name": settings.app_name,
            "version": settings.app_version,
            "description": "Plataforma digital para gestionar eventos corporativos",
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health"
        }
    )


# API information endpoint
@app.get("/api/v1", response_model=BaseResponse, tags=["api"])
async def api_info():
    """
    API v1 information endpoint.
    """
    return BaseResponse(
        success=True,
        message="App Convention API v1",
        data={
            "version": "v1",
            "endpoints": {
                "authentication": "/api/v1/auth",
                "posts": "/api/v1/posts", 
                "stories": "/api/v1/stories"
            },
            "features": [
                "JWT Authentication",
                "Role-based access control",
                "Post management",
                "Temporary stories (24h)",
                "Push notifications",
                "Real-time interactions"
            ]
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    ) 