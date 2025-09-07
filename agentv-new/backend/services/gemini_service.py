import google.generativeai as genai
from config import config
import uuid
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def create_agent_prompt(self, agent_data):
        """Generate system prompt for new agent using Gemini"""
        try:
            prompt = f"""Create a detailed system prompt for an AI agent with these specifications:
Name: {agent_data.name}
Description: {agent_data.description}
Category: {agent_data.category}

The system prompt should define the agent's personality, capabilities, and behavioral guidelines. Keep it concise but comprehensive."""

            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            logger.error(f"Failed to create agent prompt: {str(e)}")
            raise

    async def extract_skills(self, description: str):
        """Extract skills from agent description using Gemini"""
        try:
            skills_prompt = f"Based on this agent description: '{description}', list 3-5 key skills this agent would need. Return only a comma-separated list of skills."

            skills_response = self.model.generate_content(skills_prompt)
            skills_text = skills_response.text.strip()
            skills = [skill.strip() for skill in skills_text.split(',') if skill.strip()]
            return skills

        except Exception as e:
            logger.error(f"Failed to extract skills: {str(e)}")
            raise

    async def chat_with_agent(self, system_prompt: str, message: str, session_id: str = None):
        """Chat with an agent using Gemini"""
        try:
            if not session_id:
                session_id = str(uuid.uuid4())

            # Create a chat session with the system prompt
            chat = self.model.start_chat(history=[])

            # Send system prompt first
            chat.send_message(f"System: {system_prompt}")
            # Then send user message
            response = chat.send_message(message)

            return response.text.strip(), session_id

        except Exception as e:
            logger.error(f"Failed to chat with agent: {str(e)}")
            raise

gemini_service = GeminiService()
