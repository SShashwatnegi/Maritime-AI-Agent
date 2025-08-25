import React, { useState, useEffect } from 'react';
import { Ship, Bot, Zap, Activity } from 'lucide-react';
import AgentChat from './components/AgentChat';
import DirectTools from './components/DirectTools';
import AgentStatus from './components/AgentStatus';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('agent');
  const [apiHealth, setApiHealth] = useState(null);
  
  // Persistent state for conversations
  const [agentConversation, setAgentConversation] = useState([]);
  const [directToolsResponses, setDirectToolsResponses] = useState([]);

  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/ping');
      const data = await response.json();
      setApiHealth(data.status === 'healthy');
    } catch (error) {
      console.error('API health check failed:', error);
      setApiHealth(false);
    }
  };

  const tabs = [
    { id: 'agent', label: 'AI Agent', icon: Bot, description: 'Intelligent maritime assistant' },
    { id: 'tools', label: 'Direct Tools', icon: Zap, description: 'Quick access tools' },
    { id: 'status', label: 'System Status', icon: Activity, description: 'Agent health & metrics' }
  ];

  // Function to add a new message to agent conversation
  const addAgentMessage = (message) => {
    setAgentConversation(prev => [...prev, {
      id: Date.now(),
      timestamp: new Date(),
      ...message
    }]);
  };

  // Function to add a new response to direct tools
  const addDirectToolsResponse = (response) => {
    setDirectToolsResponses(prev => [...prev, {
      id: Date.now(),
      timestamp: new Date(),
      ...response
    }]);
  };

  // Function to clear conversation history
  const clearAgentConversation = () => {
    setAgentConversation([]);
  };

  const clearDirectToolsResponses = () => {
    setDirectToolsResponses([]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <header className="maritime-gradient text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Ship className="h-8 w-8" />
              <div>
                <h1 className="text-2xl font-bold">Maritime AI Agent</h1>
                <p className="text-blue-100 text-sm">Intelligent Maritime Operations Assistant</p>
              </div>
            </div>
            
            {/* API Status Indicator */}
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${apiHealth ? 'bg-green-400' : 'bg-red-400'} animate-pulse`}></div>
              <span className="text-sm">
                {apiHealth ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-1 py-4">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const hasMessages = tab.id === 'agent' ? agentConversation.length > 0 : 
                                 tab.id === 'tools' ? directToolsResponses.length > 0 : false;
              
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all duration-200 relative ${
                    activeTab === tab.id ? 'tab-active' : 'tab-inactive'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                  {/* Message indicator */}
                  {hasMessages && (
                    <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full border-2 border-white"></div>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          {/* Tab Description */}
          <div className="text-center">
            <p className="text-gray-600">
              {tabs.find(tab => tab.id === activeTab)?.description}
            </p>
          </div>

          {/* Tab Content */}
          <div className="min-h-[600px]">
            {activeTab === 'agent' && (
              <AgentChat 
                conversation={agentConversation}
                onAddMessage={addAgentMessage}
                onClearConversation={clearAgentConversation}
              />
            )}
            {activeTab === 'tools' && (
              <DirectTools 
                responses={directToolsResponses}
                onAddResponse={addDirectToolsResponse}
                onClearResponses={clearDirectToolsResponses}
              />
            )}
            {activeTab === 'status' && <AgentStatus />}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-50 border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-500 text-sm">
            <p>Maritime AI Agent v2.0 - Powered by Advanced AI Technology</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;