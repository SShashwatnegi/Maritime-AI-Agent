from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# ✅ Load .env first
load_dotenv()

async def ask_ai(prompt: str, max_tokens: int = 256):
    # ✅ Read the API key properly
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        api_key=api_key,  # ✅ must be api_key
        temperature=0
    )

    try:
        response = await llm.ainvoke(prompt)
        return response.content if hasattr(response, "content") else str(response)
    except Exception as e:
        return f"AI error: {e}"
