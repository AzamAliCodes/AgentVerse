from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes.api import api_router
from database import close_db_client
from config import config
import logging

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the main app
app = FastAPI(
    title="AgentVerse API",
    description="AI Agent Management and Chat Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=config.CORS_ORIGINS.split(',') if config.CORS_ORIGINS != '*' else ['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    logger.info("AgentVerse API started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    await close_db_client()
    logger.info("AgentVerse API shut down successfully")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host=config.HOST,
        port=config.PORT,
        reload=True
    )
