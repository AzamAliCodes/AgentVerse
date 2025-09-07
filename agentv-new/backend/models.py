from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
import uuid

class Agent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    category: str
    skills: List[str]
    system_prompt: str
    rating: float = 0.0
    downloads: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_prebuilt: bool = True

class AgentCreate(BaseModel):
    name: str
    description: str
    category: str

class AgentChat(BaseModel):
    agent_id: str
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

class UserAgent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    agent_id: str
    customizations: dict = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

def prepare_for_mongo(data):
    """Helper function for date serialization"""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
    return data
