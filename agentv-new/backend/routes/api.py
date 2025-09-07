from fastapi import APIRouter, HTTPException
from typing import List
from models import Agent, AgentCreate, AgentChat, ChatResponse, prepare_for_mongo
from services.agent_service import (
    initialize_prebuilt_agents,
    get_agents,
    get_prebuilt_agents,
    get_agent_by_id,
    create_agent,
    increment_download_count,
)
from services.gemini_service import gemini_service
import uuid

api_router = APIRouter(prefix="/api")

# Prebuilt agents data
prebuilt_agents = [
    Agent(
        name="Data Analyst Pro",
        description="Analyzes complex datasets and generates comprehensive reports with actionable insights.",
        category="Analytics",
        skills=["Python", "SQL", "Visualization"],
        system_prompt="You are a professional data analyst. Analyze data comprehensively and provide clear, actionable insights with proper visualizations and recommendations.",
        rating=4.9,
        downloads=2300
    ),
    Agent(
        name="Customer Support AI",
        description="Handles customer inquiries with empathy and provides accurate, helpful responses.",
        category="Support",
        skills=["Communication", "Problem Solving", "Multilingual"],
        system_prompt="You are a helpful customer support agent. Respond with empathy, provide accurate information, and always aim to resolve customer issues effectively.",
        rating=4.8,
        downloads=1800
    ),
    Agent(
        name="Code Reviewer",
        description="Reviews code for bugs, performance issues, and best practices across multiple languages.",
        category="Development",
        skills=["JavaScript", "Python", "Security"],
        system_prompt="You are an expert code reviewer. Analyze code for bugs, security issues, performance problems, and adherence to best practices. Provide constructive feedback.",
        rating=4.7,
        downloads=1500
    ),
    Agent(
        name="Personal Finance Advisor",
        description="Helps manage personal finances, create budgets, track expenses, and provide investment advice.",
        category="Finance",
        skills=["Budgeting", "Investment", "Tax Planning"],
        system_prompt="You are a personal finance advisor. Help users manage their money wisely, create budgets, understand investments, and make informed financial decisions.",
        rating=4.6,
        downloads=1400
    ),
    Agent(
        name="Health & Wellness Coach",
        description="Provides personalized health advice, fitness plans, nutrition guidance, and mental wellness support.",
        category="Healthcare",
        skills=["Nutrition", "Fitness", "Mental Health"],
        system_prompt="You are a health and wellness coach. Provide evidence-based health advice, create personalized fitness and nutrition plans, and support mental wellness.",
        rating=4.8,
        downloads=1650
    ),
    Agent(
        name="Creative Writing Assistant",
        description="Helps with storytelling, character development, plot creation, and overcoming writer's block.",
        category="Creative",
        skills=["Storytelling", "Character Development", "Editing"],
        system_prompt="You are a creative writing assistant. Help writers develop compelling stories, create memorable characters, overcome writer's block, and improve their craft.",
        rating=4.5,
        downloads=1200
    ),
    Agent(
        name="Learning Tutor",
        description="Provides personalized education support across various subjects with adaptive teaching methods.",
        category="Education",
        skills=["Mathematics", "Science", "Language Arts"],
        system_prompt="You are an adaptive learning tutor. Explain complex concepts clearly, adapt to different learning styles, and help students achieve their academic goals.",
        rating=4.7,
        downloads=1350
    ),
    Agent(
        name="Travel Planning Expert",
        description="Creates detailed travel itineraries, finds deals, and provides local insights for any destination.",
        category="Travel",
        skills=["Itinerary Planning", "Budget Optimization", "Cultural Insights"],
        system_prompt="You are a travel planning expert. Create amazing itineraries, find the best deals, provide local insights, and help travelers have unforgettable experiences.",
        rating=4.6,
        downloads=1100
    ),
    Agent(
        name="Productivity Optimizer",
        description="Helps organize tasks, manage time effectively, and optimize workflows for maximum productivity.",
        category="Productivity",
        skills=["Time Management", "Task Organization", "Workflow Design"],
        system_prompt="You are a productivity optimizer. Help users organize their tasks, manage time effectively, eliminate distractions, and create efficient workflows.",
        rating=4.4,
        downloads=950
    ),
    Agent(
        name="Legal Research Assistant",
        description="Assists with legal research, document review, and provides general legal information and guidance.",
        category="Legal",
        skills=["Legal Research", "Document Analysis", "Case Law"],
        system_prompt="You are a legal research assistant. Help with legal research, analyze documents, explain legal concepts clearly, but always remind users to consult qualified attorneys for legal advice.",
        rating=4.3,
        downloads=800
    ),
    Agent(
        name="HR Strategy Consultant",
        description="Provides HR guidance on recruitment, employee engagement, performance management, and workplace culture.",
        category="HR",
        skills=["Recruitment", "Employee Relations", "Performance Management"],
        system_prompt="You are an HR strategy consultant. Provide guidance on recruitment, employee engagement, performance management, and building positive workplace culture.",
        rating=4.5,
        downloads=750
    ),
    Agent(
        name="Cybersecurity Analyst",
        description="Analyzes security threats, provides risk assessments, and recommends security best practices.",
        category="Security",
        skills=["Threat Analysis", "Risk Assessment", "Security Protocols"],
        system_prompt="You are a cybersecurity analyst. Analyze security threats, assess risks, recommend security measures, and help organizations protect their digital assets.",
        rating=4.6,
        downloads=900
    )
]

@api_router.get("/")
async def root():
    return {"message": "AgentVerse API is running"}

@api_router.get("/agents", response_model=List[Agent])
async def get_agents_route():
    agents = await get_agents()
    return agents

@api_router.get("/agents/prebuilt", response_model=List[Agent])
async def get_prebuilt_agents_route():
    agents = await get_prebuilt_agents()
    return agents

@api_router.post("/agents/create", response_model=Agent)
async def create_custom_agent(agent_data: AgentCreate):
    try:
        system_prompt = await gemini_service.create_agent_prompt(agent_data)
        skills = await gemini_service.extract_skills(agent_data.description)

        new_agent = Agent(
            name=agent_data.name,
            description=agent_data.description,
            category=agent_data.category,
            skills=skills,
            system_prompt=system_prompt,
            is_prebuilt=False
        )

        created_agent = await create_agent(new_agent)
        return created_agent

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create agent: {str(e)}")

@api_router.post("/agents/chat", response_model=ChatResponse)
async def chat_with_agent(chat_request: AgentChat):
    try:
        agent = await get_agent_by_id(chat_request.agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        session_id = chat_request.session_id or str(uuid.uuid4())
        response, session_id = await gemini_service.chat_with_agent(agent.system_prompt, chat_request.message, session_id)

        return ChatResponse(response=response, session_id=session_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@api_router.get("/agents/{agent_id}/deploy")
async def deploy_agent(agent_id: str):
    agent = await get_agent_by_id(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    await increment_download_count(agent_id)
    return {"message": f"Agent {agent.name} deployed successfully", "agent_id": agent_id}

@api_router.on_event("startup")
async def startup_event():
    await initialize_prebuilt_agents(prebuilt_agents)
