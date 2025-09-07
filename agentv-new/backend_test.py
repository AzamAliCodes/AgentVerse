#!/usr/bin/env python3
"""
AgentVerse Backend API Testing Suite
Tests all backend endpoints for the AgentVerse platform
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')
load_dotenv('/app/backend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://ai-creator-hub-39.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class AgentVerseAPITester:
    def __init__(self):
        self.session = None
        self.test_results = {}
        self.created_agent_id = None
        self.chat_session_id = None
        
    async def setup_session(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'Content-Type': 'application/json'}
        )
        
    async def cleanup_session(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            
    async def test_api_health(self):
        """Test basic API connectivity"""
        print(f"\n🔍 Testing API Health Check...")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"API Base: {API_BASE}")
        
        try:
            async with self.session.get(f"{API_BASE}/") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ API Health Check: {data}")
                    self.test_results['api_health'] = True
                    return True
                else:
                    print(f"❌ API Health Check failed: Status {response.status}")
                    self.test_results['api_health'] = False
                    return False
        except Exception as e:
            print(f"❌ API Health Check failed: {str(e)}")
            self.test_results['api_health'] = False
            return False
            
    async def test_prebuilt_agents_management(self):
        """Test prebuilt agents endpoints"""
        print(f"\n🤖 Testing Prebuilt Agents Management...")
        
        # Test GET /api/agents
        try:
            async with self.session.get(f"{API_BASE}/agents") as response:
                if response.status == 200:
                    agents = await response.json()
                    print(f"✅ GET /api/agents: Found {len(agents)} agents")
                    
                    # Verify agent structure
                    if agents and len(agents) > 0:
                        agent = agents[0]
                        required_fields = ['id', 'name', 'description', 'category', 'skills', 'system_prompt']
                        missing_fields = [field for field in required_fields if field not in agent]
                        if missing_fields:
                            print(f"⚠️ Missing fields in agent: {missing_fields}")
                        else:
                            print(f"✅ Agent structure validation passed")
                    
                    self.test_results['get_all_agents'] = True
                else:
                    print(f"❌ GET /api/agents failed: Status {response.status}")
                    self.test_results['get_all_agents'] = False
        except Exception as e:
            print(f"❌ GET /api/agents failed: {str(e)}")
            self.test_results['get_all_agents'] = False
            
        # Test GET /api/agents/prebuilt
        try:
            async with self.session.get(f"{API_BASE}/agents/prebuilt") as response:
                if response.status == 200:
                    prebuilt_agents = await response.json()
                    print(f"✅ GET /api/agents/prebuilt: Found {len(prebuilt_agents)} prebuilt agents")
                    
                    # Verify all are prebuilt
                    non_prebuilt = [agent for agent in prebuilt_agents if not agent.get('is_prebuilt', True)]
                    if non_prebuilt:
                        print(f"⚠️ Found {len(non_prebuilt)} non-prebuilt agents in prebuilt endpoint")
                    else:
                        print(f"✅ All agents are correctly marked as prebuilt")
                        
                    # Expected prebuilt agents
                    expected_agents = [
                        "Data Analyst Pro", "Customer Support AI", "Code Reviewer",
                        "Project Coordinator", "Research Assistant", "Marketing Strategist"
                    ]
                    
                    found_agents = [agent['name'] for agent in prebuilt_agents]
                    missing_agents = [name for name in expected_agents if name not in found_agents]
                    
                    if missing_agents:
                        print(f"⚠️ Missing expected prebuilt agents: {missing_agents}")
                    else:
                        print(f"✅ All expected prebuilt agents found")
                    
                    self.test_results['get_prebuilt_agents'] = True
                else:
                    print(f"❌ GET /api/agents/prebuilt failed: Status {response.status}")
                    self.test_results['get_prebuilt_agents'] = False
        except Exception as e:
            print(f"❌ GET /api/agents/prebuilt failed: {str(e)}")
            self.test_results['get_prebuilt_agents'] = False
            
    async def test_custom_agent_creation(self):
        """Test custom agent creation with Gemini integration"""
        print(f"\n🛠️ Testing Custom Agent Creation...")
        
        # Test data for agent creation
        test_agent = {
            "name": "Personal Finance Advisor",
            "description": "An AI agent that helps users manage their personal finances, create budgets, track expenses, and provide investment advice based on their financial goals and risk tolerance.",
            "category": "Finance"
        }
        
        try:
            async with self.session.post(
                f"{API_BASE}/agents/create",
                json=test_agent
            ) as response:
                if response.status == 200:
                    created_agent = await response.json()
                    print(f"✅ POST /api/agents/create: Agent created successfully")
                    print(f"   Agent ID: {created_agent['id']}")
                    print(f"   Agent Name: {created_agent['name']}")
                    print(f"   Generated Skills: {created_agent['skills']}")
                    print(f"   System Prompt Length: {len(created_agent['system_prompt'])} characters")
                    
                    # Store agent ID for later tests
                    self.created_agent_id = created_agent['id']
                    
                    # Verify required fields
                    required_fields = ['id', 'name', 'description', 'category', 'skills', 'system_prompt']
                    missing_fields = [field for field in required_fields if field not in created_agent]
                    if missing_fields:
                        print(f"⚠️ Missing fields in created agent: {missing_fields}")
                    
                    # Verify Gemini integration worked
                    if created_agent['system_prompt'] and len(created_agent['system_prompt']) > 50:
                        print(f"✅ Gemini integration: System prompt generated successfully")
                        self.test_results['gemini_integration'] = True
                    else:
                        print(f"❌ Gemini integration: System prompt too short or empty")
                        self.test_results['gemini_integration'] = False
                        
                    if created_agent['skills'] and len(created_agent['skills']) > 0:
                        print(f"✅ Gemini integration: Skills generated successfully")
                    else:
                        print(f"❌ Gemini integration: No skills generated")
                        
                    # Verify it's marked as custom (not prebuilt)
                    if not created_agent.get('is_prebuilt', True):
                        print(f"✅ Agent correctly marked as custom (not prebuilt)")
                    else:
                        print(f"⚠️ Agent incorrectly marked as prebuilt")
                    
                    self.test_results['custom_agent_creation'] = True
                else:
                    error_text = await response.text()
                    print(f"❌ POST /api/agents/create failed: Status {response.status}")
                    print(f"   Error: {error_text}")
                    self.test_results['custom_agent_creation'] = False
                    self.test_results['gemini_integration'] = False
        except Exception as e:
            print(f"❌ POST /api/agents/create failed: {str(e)}")
            self.test_results['custom_agent_creation'] = False
            self.test_results['gemini_integration'] = False
            
    async def test_agent_chat_system(self):
        """Test agent chat functionality"""
        print(f"\n💬 Testing Agent Chat System...")
        
        # First, get an agent to chat with (use prebuilt agent)
        try:
            async with self.session.get(f"{API_BASE}/agents/prebuilt") as response:
                if response.status == 200:
                    agents = await response.json()
                    if agents:
                        test_agent = agents[0]  # Use first prebuilt agent
                        agent_id = test_agent['id']
                        agent_name = test_agent['name']
                        
                        print(f"Testing chat with agent: {agent_name}")
                        
                        # Test chat without session ID (new session)
                        chat_request = {
                            "agent_id": agent_id,
                            "message": "Hello! Can you introduce yourself and tell me what you can help me with?"
                        }
                        
                        async with self.session.post(
                            f"{API_BASE}/agents/chat",
                            json=chat_request
                        ) as chat_response:
                            if chat_response.status == 200:
                                chat_data = await chat_response.json()
                                print(f"✅ POST /api/agents/chat (new session): Success")
                                print(f"   Response length: {len(chat_data['response'])} characters")
                                print(f"   Session ID: {chat_data['session_id']}")
                                
                                # Store session ID for follow-up test
                                self.chat_session_id = chat_data['session_id']
                                
                                # Verify response structure
                                if 'response' in chat_data and 'session_id' in chat_data:
                                    print(f"✅ Chat response structure valid")
                                else:
                                    print(f"❌ Chat response missing required fields")
                                
                                # Test follow-up message with session ID
                                followup_request = {
                                    "agent_id": agent_id,
                                    "message": "That's great! Can you give me a specific example of how you would help?",
                                    "session_id": self.chat_session_id
                                }
                                
                                async with self.session.post(
                                    f"{API_BASE}/agents/chat",
                                    json=followup_request
                                ) as followup_response:
                                    if followup_response.status == 200:
                                        followup_data = await followup_response.json()
                                        print(f"✅ POST /api/agents/chat (existing session): Success")
                                        print(f"   Follow-up response length: {len(followup_data['response'])} characters")
                                        
                                        # Verify session continuity
                                        if followup_data['session_id'] == self.chat_session_id:
                                            print(f"✅ Session continuity maintained")
                                        else:
                                            print(f"⚠️ Session ID changed unexpectedly")
                                            
                                        self.test_results['agent_chat_system'] = True
                                    else:
                                        error_text = await followup_response.text()
                                        print(f"❌ Follow-up chat failed: Status {followup_response.status}")
                                        print(f"   Error: {error_text}")
                                        self.test_results['agent_chat_system'] = False
                            else:
                                error_text = await chat_response.text()
                                print(f"❌ POST /api/agents/chat failed: Status {chat_response.status}")
                                print(f"   Error: {error_text}")
                                self.test_results['agent_chat_system'] = False
                    else:
                        print(f"❌ No agents available for chat testing")
                        self.test_results['agent_chat_system'] = False
                else:
                    print(f"❌ Could not fetch agents for chat testing")
                    self.test_results['agent_chat_system'] = False
        except Exception as e:
            print(f"❌ Agent chat system test failed: {str(e)}")
            self.test_results['agent_chat_system'] = False
            
    async def test_agent_deploy_system(self):
        """Test agent deployment functionality"""
        print(f"\n🚀 Testing Agent Deploy System...")
        
        # Get an agent to deploy (use prebuilt agent)
        try:
            async with self.session.get(f"{API_BASE}/agents/prebuilt") as response:
                if response.status == 200:
                    agents = await response.json()
                    if agents:
                        test_agent = agents[0]  # Use first prebuilt agent
                        agent_id = test_agent['id']
                        agent_name = test_agent['name']
                        initial_downloads = test_agent.get('downloads', 0)
                        
                        print(f"Testing deployment of agent: {agent_name}")
                        print(f"Initial downloads: {initial_downloads}")
                        
                        # Test deployment
                        async with self.session.get(f"{API_BASE}/agents/{agent_id}/deploy") as deploy_response:
                            if deploy_response.status == 200:
                                deploy_data = await deploy_response.json()
                                print(f"✅ GET /api/agents/{agent_id}/deploy: Success")
                                print(f"   Deploy message: {deploy_data['message']}")
                                print(f"   Agent ID: {deploy_data['agent_id']}")
                                
                                # Verify download count increment by fetching agent again
                                async with self.session.get(f"{API_BASE}/agents") as verify_response:
                                    if verify_response.status == 200:
                                        updated_agents = await verify_response.json()
                                        updated_agent = next((a for a in updated_agents if a['id'] == agent_id), None)
                                        
                                        if updated_agent:
                                            new_downloads = updated_agent.get('downloads', 0)
                                            print(f"   Updated downloads: {new_downloads}")
                                            
                                            if new_downloads == initial_downloads + 1:
                                                print(f"✅ Download count incremented correctly")
                                                self.test_results['agent_deploy_system'] = True
                                            else:
                                                print(f"⚠️ Download count not incremented as expected")
                                                self.test_results['agent_deploy_system'] = False
                                        else:
                                            print(f"❌ Could not find agent after deployment")
                                            self.test_results['agent_deploy_system'] = False
                                    else:
                                        print(f"❌ Could not verify download count update")
                                        self.test_results['agent_deploy_system'] = False
                            else:
                                error_text = await deploy_response.text()
                                print(f"❌ Agent deployment failed: Status {deploy_response.status}")
                                print(f"   Error: {error_text}")
                                self.test_results['agent_deploy_system'] = False
                                
                        # Test deployment of non-existent agent
                        fake_agent_id = "non-existent-agent-id"
                        async with self.session.get(f"{API_BASE}/agents/{fake_agent_id}/deploy") as fake_deploy_response:
                            if fake_deploy_response.status == 404:
                                print(f"✅ Deployment of non-existent agent correctly returns 404")
                            else:
                                print(f"⚠️ Deployment of non-existent agent should return 404, got {fake_deploy_response.status}")
                                
                    else:
                        print(f"❌ No agents available for deployment testing")
                        self.test_results['agent_deploy_system'] = False
                else:
                    print(f"❌ Could not fetch agents for deployment testing")
                    self.test_results['agent_deploy_system'] = False
        except Exception as e:
            print(f"❌ Agent deploy system test failed: {str(e)}")
            self.test_results['agent_deploy_system'] = False
            
    async def test_error_handling(self):
        """Test API error handling"""
        print(f"\n🛡️ Testing Error Handling...")
        
        # Test chat with non-existent agent
        try:
            chat_request = {
                "agent_id": "non-existent-agent",
                "message": "Hello"
            }
            
            async with self.session.post(
                f"{API_BASE}/agents/chat",
                json=chat_request
            ) as response:
                if response.status == 404:
                    print(f"✅ Chat with non-existent agent correctly returns 404")
                else:
                    print(f"⚠️ Chat with non-existent agent should return 404, got {response.status}")
        except Exception as e:
            print(f"⚠️ Error handling test failed: {str(e)}")
            
    def print_summary(self):
        """Print test results summary"""
        print(f"\n" + "="*60)
        print(f"🧪 AGENTVERSE BACKEND TEST RESULTS SUMMARY")
        print(f"="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\nDetailed Results:")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {test_name}: {status}")
            
        # Critical issues summary
        critical_failures = []
        if not self.test_results.get('api_health', False):
            critical_failures.append("API Health Check - Backend not accessible")
        if not self.test_results.get('gemini_integration', False):
            critical_failures.append("Gemini LLM Integration - AI functionality not working")
        if not self.test_results.get('get_prebuilt_agents', False):
            critical_failures.append("Prebuilt Agents - Core agents not available")
        if not self.test_results.get('custom_agent_creation', False):
            critical_failures.append("Custom Agent Creation - Cannot create new agents")
        if not self.test_results.get('agent_chat_system', False):
            critical_failures.append("Agent Chat System - Chat functionality broken")
            
        if critical_failures:
            print(f"\n🚨 CRITICAL ISSUES FOUND:")
            for issue in critical_failures:
                print(f"  • {issue}")
        else:
            print(f"\n🎉 All critical systems are working!")
            
        print(f"="*60)
        
    async def run_all_tests(self):
        """Run all backend tests"""
        print(f"🚀 Starting AgentVerse Backend API Tests")
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        await self.setup_session()
        
        try:
            # Test in order of dependency
            await self.test_api_health()
            
            if self.test_results.get('api_health', False):
                await self.test_prebuilt_agents_management()
                await self.test_custom_agent_creation()
                await self.test_agent_chat_system()
                await self.test_agent_deploy_system()
                await self.test_error_handling()
            else:
                print(f"\n❌ Skipping remaining tests due to API health check failure")
                
        finally:
            await self.cleanup_session()
            
        self.print_summary()
        return self.test_results

async def main():
    """Main test runner"""
    tester = AgentVerseAPITester()
    results = await tester.run_all_tests()
    
    # Return exit code based on critical test results
    critical_tests = ['api_health', 'gemini_integration', 'get_prebuilt_agents', 'custom_agent_creation', 'agent_chat_system']
    critical_failures = [test for test in critical_tests if not results.get(test, False)]
    
    if critical_failures:
        print(f"\n❌ Critical tests failed: {critical_failures}")
        return 1
    else:
        print(f"\n✅ All critical tests passed!")
        return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)