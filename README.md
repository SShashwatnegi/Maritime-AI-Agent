Maritime AI Agent

This project is an AI-powered maritime assistant built using LangChain and Google Gemini. It combines natural language processing with domain-specific tools to support decision-making in shipping and port operations.

Key Features

Conversational AI – Ask natural language questions and get contextual responses.

Weather Forecasting – Retrieve forecasts for any city or geographic coordinates.

Bad Weather Detection – Identify periods of rain, storm, fog, or snow that may impact voyages.

Laytime Calculator – Compute laytime based on cargo details and contractual terms.

Document Summarization – Upload maritime-related PDF, DOCX, or TXT documents and receive concise summaries.

Memory System – Retains conversation history for context-aware responses.

Tech Stack

LLM: Google Gemini (gemini-1.5-flash)

Framework: LangChain

Backend API: FastAPI

Services: Custom Weather API, Laytime Calculator, Document Summarizer

Memory: ConversationBufferMemory

 How It Works

The user sends a query to the API.

The agent decides whether to respond directly or call one of the registered tools.

Tools fetch weather data, calculate laytime, or summarize documents.

The agent integrates the result into a natural language response.

Memory ensures continuity across multi-turn conversations.

This assistant is designed for maritime professionals, port authorities, and shipping companies to improve operational efficiency and decision-making by combining AI reasoning with domain-specific tools.Maritime AI Agent Frontend Summary


Overview
The Maritime AI Agent Frontend is a modern, responsive web application built with React 18.2+ and Hooks, designed to interact with AI-powered maritime tools. It integrates with a backend to provide intelligent conversations, document analysis, weather monitoring, and system status tracking, tailored for maritime operations. The application uses Tailwind CSS for styling, Lucide React for icons, Axios for API calls, and is built with Create React App (CRA) using npm.
Key Features
AI Agent Interface

Intelligent Conversations: Context-aware chat with maritime expertise.
Document Upload & Analysis: Supports PDF, Word, Excel, and text files.
Reasoning Transparency: Displays AI thought processes and tool usage.
Memory Management: Persistent conversation context with clear management options.

Direct Tools Access

Quick Ask: Fast answers to maritime questions.
Document Summarization: Instant extraction of key document insights.
Weather Data: Real-time, maritime-specific weather conditions.
Geolocation Support: Auto-detects location for relevant weather data.

System Monitoring

Agent Status: Real-time health and performance monitoring.
Tool Availability: Status and details of available tools.
Performance Analytics: Compares AI agent and direct tool performance.
Error Tracking: Detailed error logs for debugging.

Technology Stack

Frontend: React 18.2+ with Hooks.
Styling: Tailwind CSS for responsive design.
Icons: Lucide React for consistent iconography.
HTTP Client: Axios for API communication.
Build Tool: Create React App (CRA).
Package Manager: npm.

Purpose
The Maritime AI Agent Frontend provides maritime professionals with an intuitive, AI-driven interface to enhance operational decision-making through intelligent insights, real-time data, and system transparency, all tailored to the maritime industry’s needs.
