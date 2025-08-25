from datetime import datetime
from typing import Any, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from app.services.weather import WeatherService
from app.services.laytime import LaytimeCalculator
from app.services.documents import summarize_document
import asyncio
import os
from dotenv import load_dotenv

class MaritimeLangChainAgent:
    def __init__(self, api_key: str):
        # Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",   # ✅ use supported Gemini model
            google_api_key=api_key,
            temperature=0
        )

        # Conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Services
        self.weather_service = WeatherService()

        # Tools
        tools = [
            Tool(
                name="Weather Forecast",
                func=self.weather_forecast_tool,
                description="Get weather forecast for a city name or 'lat,lon'"
            ),
            Tool(
                name="Bad Weather Periods",
                func=self.bad_weather_tool,
                description="Get periods of bad weather (rain, storm, fog, snow) for a location"
            ),
            Tool(
                name="Laytime Calculator",
                func=lambda params: LaytimeCalculator().calculate(params),  # ✅ fixed
                description="Calculate laytime based on cargo details and laytime terms"
            ),
            Tool(
                name="Document Summarizer",
                func=lambda file: asyncio.run(summarize_document(file)),  # ✅ Added document tool
                description="Upload and summarize maritime PDF/DOCX/TXT documents"
            ),
        ]

        # Agent setup
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent="conversational-react-description",
            memory=self.memory,
            verbose=True
        )

    # Weather tool
    def weather_forecast_tool(self, location: str, hours: int = 48):
        try:
            forecast = self.weather_service.forecast_by_location(location, hours)
            formatted = f"Weather forecast for {location}:\n"
            for entry in forecast:
                dt = datetime.fromisoformat(entry["time"])
                formatted += f"- {dt.strftime('%Y-%m-%d %H:%M')}: {entry['condition']}, {entry['temperature']}°C\n"
            return formatted
        except Exception as e:
            return f"Error fetching weather: {str(e)}"

    # Bad weather tool
    def bad_weather_tool(self, location: str, hours: int = 48):
        try:
            periods = self.weather_service.bad_periods_by_location(location, hours)
            if not periods:
                return f"No bad weather expected in the next {hours} hours at {location}."
            formatted = f"Bad weather periods for {location}:\n"
            for start, end in periods:
                start_dt = datetime.fromisoformat(start)
                end_dt = datetime.fromisoformat(end)
                formatted += f"- From {start_dt.strftime('%Y-%m-%d %H:%M')} to {end_dt.strftime('%Y-%m-%d %H:%M')}\n"
            return formatted
        except Exception as e:
            return f"Error fetching bad weather periods: {str(e)}"

    # Async process_query
    async def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
        try:
            # ✅ directly use async run
            answer = await self.agent.arun(query)
            return {
                "answer": answer,
                "tools_used": [tool.name for tool in self.agent.tools],  # ✅ crude tracking
                "execution_plan": "Handled by conversational-react agent",
                "confidence": 1.0,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

    # Status check
    def get_status(self) -> Dict[str, Any]:
        return {
            "status": "operational",
            "memory_trace": [msg.content for msg in self.memory.chat_memory.messages],
            "last_updated": datetime.now().isoformat()
        }

    # Memory reset
    def clear_memory(self) -> Dict[str, Any]:
        self.memory.clear()
        return {"message": "Memory cleared successfully."}
