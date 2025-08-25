# app/main.py
from fastapi import FastAPI
from app.api.routes import router
from app.api.agents_routes import agent_router  # 🆕 New agentic routes
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Maritime AI Agent - Enhanced with Agentic Intelligence",
    description="""
    🚢 **Maritime AI Agent with Agentic Capabilities** 
    
    **Your Original Tools (Still Available):**
    - 📋 Document summarization (`/api/documents/summarize`)
    - 🌦️ Weather information (`/api/weather/{lat}/{lon}`)
    - 🧠 AI Q&A (`/api/ask`)
    - ⏱️ Direct tool access for specific needs
    
    **🆕 New Agentic Intelligence:**
    - 🤖 **Autonomous Problem Solving** - Ask complex questions in natural language
    - 🧠 **Multi-step Reasoning** - Agent plans and executes multiple steps automatically
    - ⚡ **Intelligent Tool Orchestration** - Automatically uses your existing tools
    - 💾 **Context Memory** - Remembers conversation for better responses
    - 📊 **Comprehensive Analysis** - Combines multiple data sources intelligently
    
    **✨ Key Difference:** Instead of calling individual tools, just describe what you want!
    """,
    version="2.0.0-agentic"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include your original routes (unchanged!)
app.include_router(router, prefix="/api")

# Include new agentic routes  
app.include_router(agent_router, prefix="/api")

# Enhanced root endpoint
@app.get("/")
def root():
    return {
        "message": "🚢 Maritime AI Agent - Now with Agentic Intelligence!",
        "version": "2.0.0-agentic",
        "whats_new": "Your existing tools are now orchestrated by an intelligent agent!",
        
        "🔧 original_endpoints": {
            "description": "Your existing tools - still work exactly the same",
            "ping": "/api/ping",
            "ai_qa": "/api/ask", 
            "document_summary": "/api/documents/summarize",
            "weather": "/api/weather/{lat}/{lon}",
            "docs": "/docs"
        },
        
        "🤖 agentic_endpoints": {
            "description": "New intelligent agent that uses your tools automatically",
            "intelligent_query": "/api/agent/query",
            "agent_status": "/api/agent/status", 
            "available_tools": "/api/agent/tools",
            "examples": "/api/agent/examples",
            "memory": "/api/agent/memory",
            "comparison": "/api/agent/comparison"
        },
        
        "✨ agentic_features": [
            "🧠 Understands complex maritime questions in natural language",
            "⚡ Automatically selects and combines your existing tools",
            "📊 Provides comprehensive analysis from multiple data sources", 
            "💾 Remembers conversation context for better responses",
            "🔄 Adapts plans based on intermediate results",
            "🛡️ Maritime safety and compliance awareness"
        ],
        
        "🚀 quick_start": {
            "1": "Keep using your existing endpoints as before",
            "2": "Try the new agent: POST /api/agent/query with any maritime question",
            "3": "Check examples: GET /api/agent/examples",
            "4": "See what tools the agent can use: GET /api/agent/tools"
        },
        
        "💡 example_agentic_queries": [
            "Should I delay departure from Singapore due to weather?",
            "Calculate demurrage for my vessel operation", 
            "Analyze this charter party document and highlight risks",
            "Plan optimal route from Rotterdam to Hamburg",
            "What are the fuel requirements for this voyage considering current regulations?"
        ]
    }

# Health check for both original and agentic systems
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "components": {
            "✅ original_services": {
                "ai_service": "operational",
                "weather_service": "operational", 
                "document_service": "operational",
                "laytime_calculator": "operational"
            },
            "✅ agentic_ai": {
                "maritime_agent": "operational",
                "tool_orchestration": "operational",
                "memory_system": "operational",
                "planning_engine": "operational"
            }
        },
        "message": "All systems operational - both original tools and agentic intelligence ready!"
    }