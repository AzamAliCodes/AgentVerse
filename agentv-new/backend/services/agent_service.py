from database import db
from models import Agent, prepare_for_mongo
from typing import List
import logging

logger = logging.getLogger(__name__)

async def initialize_prebuilt_agents(prebuilt_agents: List[Agent]):
    existing_count = await db.agents.count_documents({"is_prebuilt": True})
    if existing_count == 0:
        for agent in prebuilt_agents:
            agent_dict = prepare_for_mongo(agent.dict())
            await db.agents.insert_one(agent_dict)
        logger.info("Prebuilt agents initialized.")
    else:
        logger.info("Prebuilt agents already exist. Skipping initialization.")

async def get_agents():
    agents = await db.agents.find().to_list(1000)
    return [Agent(**agent) for agent in agents]

async def get_prebuilt_agents():
    agents = await db.agents.find({"is_prebuilt": True}).to_list(1000)
    return [Agent(**agent) for agent in agents]

async def get_agent_by_id(agent_id: str):
    agent = await db.agents.find_one({"id": agent_id})
    return Agent(**agent) if agent else None

async def create_agent(agent: Agent):
    agent_dict = prepare_for_mongo(agent.dict())
    await db.agents.insert_one(agent_dict)
    return agent

async def increment_download_count(agent_id: str):
    await db.agents.update_one({"id": agent_id}, {"$inc": {"downloads": 1}})
