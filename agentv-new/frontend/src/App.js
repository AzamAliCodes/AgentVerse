import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [currentPage, setCurrentPage] = useState('library');
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [chatMessage, setChatMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  
  // Agent creation form
  const [newAgent, setNewAgent] = useState({
    name: '',
    description: '',
    category: 'General'
  });
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/agents/prebuilt`);
      setAgents(response.data);
    } catch (error) {
      console.error('Failed to load agents:', error);
    } finally {
      setLoading(false);
    }
  };

  const createAgent = async (e) => {
    e.preventDefault();
    if (!newAgent.description) return;
    
    // Auto-generate name if not provided
    const agentName = newAgent.name || `Custom Agent ${Date.now()}`;
    
    try {
      setIsCreating(true);
      const response = await axios.post(`${API}/agents/create`, {
        ...newAgent,
        name: agentName
      });
      setAgents([...agents, response.data]);
      setNewAgent({ name: '', description: '', category: 'General' });
      setCurrentPage('library');
      alert('Agent created successfully! Check the Agent Library.');
    } catch (error) {
      console.error('Failed to create agent:', error);
      alert('Failed to create agent. Please try again.');
    } finally {
      setIsCreating(false);
    }
  };

  const deployAgent = async (agentId) => {
    try {
      await axios.get(`${API}/agents/${agentId}/deploy`);
      // Update the agent's download count locally
      setAgents(agents.map(agent => 
        agent.id === agentId 
          ? { ...agent, downloads: agent.downloads + 1 }
          : agent
      ));
    } catch (error) {
      console.error('Failed to deploy agent:', error);
    }
  };

  const startChat = (agent) => {
    setSelectedAgent(agent);
    setChatHistory([]);
    setSessionId(null);
    setCurrentPage('chat');
  };

  // Helper function to render text with proper formatting
  const renderFormattedText = (text) => {
    return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!chatMessage.trim() || !selectedAgent) return;

    const userMessage = { text: chatMessage, sender: 'user' };
    setChatHistory(prev => [...prev, userMessage]);
    setChatMessage('');

    try {
      const response = await axios.post(`${API}/agents/chat`, {
        agent_id: selectedAgent.id,
        message: chatMessage,
        session_id: sessionId
      });

      const botMessage = { text: response.data.response, sender: 'bot' };
      setChatHistory(prev => [...prev, botMessage]);
      setSessionId(response.data.session_id);
    } catch (error) {
      console.error('Chat failed:', error);
      const errorMessage = { text: 'Sorry, I encountered an error. Please try again.', sender: 'bot' };
      setChatHistory(prev => [...prev, errorMessage]);
    }
  };

  const getCategoryIcon = (category) => {
    const icons = {
      'Analytics': '📊',
      'Support': '💬',
      'Development': '💻',
      'Management': '🎯',
      'Research': '🔍',
      'Marketing': '📈',
      'Education': '🎓',
      'Finance': '💰',
      'Healthcare': '🏥',
      'Creative': '🎨',
      'Legal': '⚖️',
      'HR': '👥',
      'Operations': '⚙️',
      'Entertainment': '🎬',
      'Travel': '✈️',
      'Productivity': '📋',
      'Security': '🛡️',
      'General': '🤖'
    };
    return icons[category] || '🤖';
  };

  const getCategoryColor = (category) => {
    const colors = {
      'Analytics': 'from-blue-500 to-cyan-500',
      'Support': 'from-green-500 to-emerald-500',
      'Development': 'from-purple-500 to-violet-500',
      'Management': 'from-orange-500 to-red-500',
      'Research': 'from-indigo-500 to-blue-500',
      'Marketing': 'from-pink-500 to-rose-500',
      'Education': 'from-yellow-500 to-orange-500',
      'Finance': 'from-green-600 to-teal-500',
      'Healthcare': 'from-red-500 to-pink-500',
      'Creative': 'from-purple-600 to-pink-500',
      'Legal': 'from-gray-600 to-slate-500',
      'HR': 'from-blue-600 to-indigo-500',
      'Operations': 'from-amber-500 to-orange-500',
      'Entertainment': 'from-magenta-500 to-purple-500',
      'Travel': 'from-sky-500 to-blue-500',
      'Productivity': 'from-lime-500 to-green-500',
      'Security': 'from-red-600 to-orange-500',
      'General': 'from-gray-500 to-slate-500'
    };
    return colors[category] || 'from-gray-500 to-slate-500';
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Navigation */}
      <nav className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <div className="text-3xl mr-2">🤖</div>
                <img 
                  src="https://github.com/user-attachments/assets/c6df6be6-0b9f-470d-a9c8-de06c0b2bb34" 
                  alt="AgentVerse Logo" 
                  className="w-10 h-10 mr-3"
                />
                <div className="text-2xl font-bold bg-gradient-to-r from-green-400 to-cyan-400 bg-clip-text text-transparent">
                  AgentVerse
                </div>
              </div>
              <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4">
                  <button
                    onClick={() => setCurrentPage('library')}
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      currentPage === 'library'
                        ? 'bg-cyan-500 text-white'
                        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                    }`}
                  >
                    Library
                  </button>
                  <button
                    onClick={() => setCurrentPage('builder')}
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      currentPage === 'builder'
                        ? 'bg-cyan-500 text-white'
                        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                    }`}
                  >
                    Builder
                  </button>
                  <button
                    onClick={() => setCurrentPage('collaboration')}
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      currentPage === 'collaboration'
                        ? 'bg-cyan-500 text-white'
                        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                    }`}
                  >
                    Collaboration
                  </button>
                </div>
              </div>
            </div>
            <div className="hidden md:block">
              <div className="ml-4 flex items-center md:ml-6">
                <button className="bg-gradient-to-r from-green-500 to-cyan-500 hover:from-green-600 hover:to-cyan-600 text-white px-4 py-2 rounded-lg font-medium transition-all duration-200">
                  Get Started
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {currentPage === 'library' && (
          <div className="px-4 py-6 sm:px-0">
            <div className="text-center mb-12">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-green-400 to-cyan-400 bg-clip-text text-transparent mb-4">
                Agent Library
              </h1>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                Discover pre-built AI agents ready to transform your workflow. Each agent is crafted by experts and battle-tested in real scenarios.
              </p>
            </div>

            {loading ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-cyan-500"></div>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {agents.map((agent) => (
                  <div
                    key={agent.id}
                    className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden hover:border-cyan-500 transition-all duration-300 transform hover:scale-105"
                  >
                    <div className={`h-2 bg-gradient-to-r ${getCategoryColor(agent.category)}`}></div>
                    <div className="p-6">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="text-xl font-semibold text-white mb-2">
                            {getCategoryIcon(agent.category)} {agent.name}
                          </h3>
                          <span className="inline-block bg-gray-700 text-gray-300 px-2 py-1 rounded text-sm">
                            {agent.category}
                          </span>
                        </div>
                      </div>
                      
                      <p className="text-gray-400 mb-4 text-sm leading-relaxed">
                        {agent.description}
                      </p>
                      
                      <div className="flex flex-wrap gap-2 mb-4">
                        {agent.skills.map((skill, index) => (
                          <span
                            key={index}
                            className="bg-gray-700 text-cyan-400 px-2 py-1 rounded text-xs"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                      
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center">
                          <span className="text-yellow-400">⭐</span>
                          <span className="ml-1 text-sm text-gray-300">{agent.rating}</span>
                        </div>
                        <div className="flex items-center text-sm text-gray-400">
                          <span>⬇️</span>
                          <span className="ml-1">{agent.downloads.toLocaleString()}</span>
                        </div>
                      </div>
                      
                      <div className="flex gap-2">
                        <button
                          onClick={() => startChat(agent)}
                          className="flex-1 bg-gradient-to-r from-green-500 to-cyan-500 hover:from-green-600 hover:to-cyan-600 text-white py-2 px-4 rounded-lg font-medium transition-all duration-200"
                        >
                          💬 Chat
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {currentPage === 'builder' && (
          <div className="px-4 py-6 sm:px-0">
            <div className="text-center mb-12">
              <h1 className="text-5xl font-bold bg-gradient-to-r from-green-400 to-cyan-400 bg-clip-text text-transparent mb-4">
                AI Agent Builder
              </h1>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                Describe your idea and watch it become a functional AI agent
              </p>
            </div>

            <div className="max-w-4xl mx-auto">
              <form onSubmit={createAgent} className="bg-gray-800/50 backdrop-blur rounded-2xl border border-gray-700/50 p-8 shadow-2xl">
                <div className="mb-8">
                  <label htmlFor="description" className="block text-lg font-medium text-gray-200 mb-4">
                    Describe your AI agent idea:
                  </label>
                  <textarea
                    id="description"
                    value={newAgent.description}
                    onChange={(e) => setNewAgent({ ...newAgent, description: e.target.value })}
                    rows={8}
                    className="w-full px-4 py-4 bg-gray-700/50 border border-gray-600/50 rounded-xl focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white text-lg leading-relaxed resize-none backdrop-blur"
                    placeholder="I want an AI agent that helps me plan healthy meals for the week, suggests recipes based on my dietary preferences, and creates shopping lists..."
                    required
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-2">
                      Agent Name (Optional)
                    </label>
                    <input
                      type="text"
                      id="name"
                      value={newAgent.name}
                      onChange={(e) => setNewAgent({ ...newAgent, name: e.target.value })}
                      className="w-full px-4 py-3 bg-gray-700/50 border border-gray-600/50 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white backdrop-blur"
                      placeholder="e.g., Meal Planning Assistant"
                    />
                  </div>

                  <div>
                    <label htmlFor="category" className="block text-sm font-medium text-gray-300 mb-2">
                      Category
                    </label>
                    <select
                      id="category"
                      value={newAgent.category}
                      onChange={(e) => setNewAgent({ ...newAgent, category: e.target.value })}
                      className="w-full px-4 py-3 bg-gray-700/50 border border-gray-600/50 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white backdrop-blur"
                    >
                      <option value="General">General</option>
                      <option value="Analytics">Analytics & Data Science</option>
                      <option value="Support">Customer Support</option>
                      <option value="Development">Software Development</option>
                      <option value="Management">Project Management</option>
                      <option value="Research">Research & Analysis</option>
                      <option value="Marketing">Marketing & Sales</option>
                      <option value="Education">Education & Training</option>
                      <option value="Finance">Finance & Accounting</option>
                      <option value="Healthcare">Healthcare & Wellness</option>
                      <option value="Creative">Creative & Design</option>
                      <option value="Legal">Legal & Compliance</option>
                      <option value="HR">Human Resources</option>
                      <option value="Operations">Operations & Logistics</option>
                      <option value="Entertainment">Entertainment & Media</option>
                      <option value="Travel">Travel & Hospitality</option>
                      <option value="Productivity">Productivity & Organization</option>
                      <option value="Security">Security & Risk</option>
                    </select>
                  </div>
                </div>

                <div className="text-center">
                  <button
                    type="submit"
                    disabled={isCreating}
                    className="bg-gradient-to-r from-green-500 to-cyan-500 hover:from-green-600 hover:to-cyan-600 disabled:from-gray-600 disabled:to-gray-600 text-white py-4 px-12 rounded-xl font-semibold text-lg transition-all duration-300 transform hover:scale-105 disabled:scale-100 shadow-lg hover:shadow-xl"
                  >
                    {isCreating ? '🔄 Creating Agent...' : 'Build My Agent'}
                  </button>
                </div>
              </form>

              {/* Inspiration Section */}
              <div className="mt-16">
                <h2 className="text-2xl font-semibold text-gray-200 mb-8 text-center">
                  Need inspiration? Try these ideas:
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  <div 
                    className="bg-gray-800/30 backdrop-blur rounded-xl p-6 border border-gray-700/30 hover:border-cyan-500/50 transition-all duration-300 cursor-pointer hover:bg-gray-800/50"
                    onClick={() => setNewAgent({
                      ...newAgent, 
                      description: "A personal finance advisor that helps manage budgets, track expenses, analyze spending patterns, provide investment recommendations, and offer personalized financial planning advice based on income and goals.",
                      category: "Finance"
                    })}
                  >
                    <div className="text-3xl mb-3">💰</div>
                    <h3 className="text-lg font-semibold text-white mb-2">Finance Advisor</h3>
                    <p className="text-gray-400 text-sm">A personal finance advisor for budgeting and investment guidance</p>
                  </div>

                  <div 
                    className="bg-gray-800/30 backdrop-blur rounded-xl p-6 border border-gray-700/30 hover:border-cyan-500/50 transition-all duration-300 cursor-pointer hover:bg-gray-800/50"
                    onClick={() => setNewAgent({
                      ...newAgent, 
                      description: "A health and wellness coach that creates personalized fitness routines, provides nutrition advice, tracks health metrics, offers mental wellness support, and helps achieve lifestyle goals.",
                      category: "Healthcare"
                    })}
                  >
                    <div className="text-3xl mb-3">🏥</div>
                    <h3 className="text-lg font-semibold text-white mb-2">Wellness Coach</h3>
                    <p className="text-gray-400 text-sm">A health and wellness coach for fitness and nutrition guidance</p>
                  </div>

                  <div 
                    className="bg-gray-800/30 backdrop-blur rounded-xl p-6 border border-gray-700/30 hover:border-cyan-500/50 transition-all duration-300 cursor-pointer hover:bg-gray-800/50"
                    onClick={() => setNewAgent({
                      ...newAgent, 
                      description: "A learning tutor that provides personalized education support, explains complex concepts in simple terms, creates study plans, offers practice exercises, and adapts to different learning styles.",
                      category: "Education"
                    })}
                  >
                    <div className="text-3xl mb-3">🎓</div>
                    <h3 className="text-lg font-semibold text-white mb-2">Learning Tutor</h3>
                    <p className="text-gray-400 text-sm">A personalized learning tutor for any subject or skill</p>
                  </div>

                  <div 
                    className="bg-gray-800/30 backdrop-blur rounded-xl p-6 border border-gray-700/30 hover:border-cyan-500/50 transition-all duration-300 cursor-pointer hover:bg-gray-800/50"
                    onClick={() => setNewAgent({
                      ...newAgent, 
                      description: "A productivity optimizer that helps organize tasks, manage time effectively, eliminate distractions, create efficient workflows, and boost overall productivity using proven methodologies.",
                      category: "Productivity"
                    })}
                  >
                    <div className="text-3xl mb-3">📋</div>
                    <h3 className="text-lg font-semibold text-white mb-2">Productivity Expert</h3>
                    <p className="text-gray-400 text-sm">A productivity optimizer for time management and task organization</p>
                  </div>

                  <div 
                    className="bg-gray-800/30 backdrop-blur rounded-xl p-6 border border-gray-700/30 hover:border-cyan-500/50 transition-all duration-300 cursor-pointer hover:bg-gray-800/50"
                    onClick={() => setNewAgent({
                      ...newAgent, 
                      description: "A legal research assistant that helps with legal document analysis, case law research, contract review, compliance guidance, and provides general legal information while advising consultation with qualified attorneys.",
                      category: "Legal"
                    })}
                  >
                    <div className="text-3xl mb-3">⚖️</div>
                    <h3 className="text-lg font-semibold text-white mb-2">Legal Assistant</h3>
                    <p className="text-gray-400 text-sm">A legal research assistant for document analysis and research</p>
                  </div>

                  <div 
                    className="bg-gray-800/30 backdrop-blur rounded-xl p-6 border border-gray-700/30 hover:border-cyan-500/50 transition-all duration-300 cursor-pointer hover:bg-gray-800/50"
                    onClick={() => setNewAgent({
                      ...newAgent, 
                      description: "A cybersecurity analyst that assesses security risks, analyzes threats, recommends security measures, reviews security protocols, and helps protect digital assets and sensitive information.",
                      category: "Security"
                    })}
                  >
                    <div className="text-3xl mb-3">🛡️</div>
                    <h3 className="text-lg font-semibold text-white mb-2">Security Analyst</h3>
                    <p className="text-gray-400 text-sm">A cybersecurity analyst for threat assessment and protection</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {currentPage === 'chat' && selectedAgent && (
          <div className="px-4 py-6 sm:px-0">
            <div className="max-w-4xl mx-auto">
              <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
                <div className="bg-gray-700 px-6 py-4 border-b border-gray-600">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <span className="text-2xl mr-3">{getCategoryIcon(selectedAgent.category)}</span>
                      <div>
                        <h2 className="text-xl font-semibold text-white">{selectedAgent.name}</h2>
                        <p className="text-gray-400 text-sm">{selectedAgent.category}</p>
                      </div>
                    </div>
                    <button
                      onClick={() => setCurrentPage('library')}
                      className="bg-gray-600 hover:bg-gray-500 text-white px-4 py-2 rounded-lg transition-colors"
                    >
                      ← Back to Library
                    </button>
                  </div>
                </div>

                <div className="h-96 overflow-y-auto p-6 space-y-4">
                  {chatHistory.length === 0 ? (
                    <div className="text-center text-gray-400 py-8">
                      <p>Start a conversation with {selectedAgent.name}</p>
                    </div>
                  ) : (
                    chatHistory.map((message, index) => (
                      <div
                        key={index}
                        className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                      >
                        <div
                          className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                            message.sender === 'user'
                              ? 'bg-gradient-to-r from-green-500 to-cyan-500 text-white'
                              : 'bg-gray-700 text-gray-100'
                          }`}
                        >
                          <div 
                            className="text-sm whitespace-pre-wrap" 
                            dangerouslySetInnerHTML={{ __html: renderFormattedText(message.text) }}
                          />
                        </div>
                      </div>
                    ))
                  )}
                </div>

                <form onSubmit={sendMessage} className="border-t border-gray-600 p-4">
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      value={chatMessage}
                      onChange={(e) => setChatMessage(e.target.value)}
                      className="flex-1 px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white"
                      placeholder="Type your message..."
                    />
                    <button
                      type="submit"
                      className="bg-gradient-to-r from-green-500 to-cyan-500 hover:from-green-600 hover:to-cyan-600 text-white px-6 py-2 rounded-lg font-medium transition-all duration-200"
                    >
                      Send
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        )}

        {currentPage === 'collaboration' && (
          <div className="px-4 py-6 sm:px-0">
            <div className="text-center mb-12">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-green-400 to-cyan-400 bg-clip-text text-transparent mb-4">
                Agent Collaboration
              </h1>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                Connect your agents to work together seamlessly. Build powerful workflows by linking multiple AI agents.
              </p>
            </div>
            <div className="text-center py-20">
              <div className="text-6xl mb-4">🔄</div>
              <p className="text-gray-400 text-lg">Coming Soon: Agent Collaboration Features</p>
              <p className="text-gray-500 mt-2">Create workflows where agents can communicate and work together</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;