# app/api/agent_router.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel
import json
from app.agents.maritime_agent import MaritimeLangChainAgent
from app.services.documents import summarize_document
from dotenv import load_dotenv
import os
import asyncio

# Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Initialize router and agent
agent_router = APIRouter()
maritime_agent = MaritimeLangChainAgent(api_key=api_key)

# Response model
class AgentQueryResponse(BaseModel):
    answer: str
    tools_used: list
    execution_plan: str
    confidence: float
    timestamp: str

# -------------------------
# Agent Query Route
# -------------------------
@agent_router.post("/agent/query", response_model=AgentQueryResponse)

async def agentic_query(
    query: str = Form(...),
    file: Optional[UploadFile] = File(None),
    context: Optional[str] = Form(None)
):
    try:
        # Parse context
        context_dict = {}
        if context:
            try:
                context_dict = json.loads(context)
            except:
                context_dict = {"note": context}

        # Summarize uploaded document if present
        if file:
            summary = await summarize_document(file)
            query = f"{query}\n\nDocument summary: {summary}"

        # Await the async process_query coroutine
        result = await maritime_agent.process_query(query)

        # Ensure result is a dict
        if isinstance(result, str):
            result = {
                "answer": result,
                "tools_used": [],
                "execution_plan": "N/A",
                "confidence": 1.0,
                "timestamp": datetime.now().isoformat()
            }

        return AgentQueryResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing error: {str(e)}")

# -------------------------
# Agent Status Route
# -------------------------
@agent_router.get("/agent/status")
async def get_agent_status():
    try:
        # get_status is sync, run in thread
        status = await asyncio.to_thread(maritime_agent.get_agent_status)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching agent status: {str(e)}")

# -------------------------
# Clear Memory Route
# -------------------------
@agent_router.post("/agent/memory/clear")
async def clear_agent_memory():
    try:
        result = await asyncio.to_thread(maritime_agent.clear_memory)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {str(e)}")
