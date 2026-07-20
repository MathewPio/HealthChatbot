import httpx
# from app.services.ollama_service import OLLAMA_MODEL, OLLAMA_URL

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2:3b"

def generate_ai_response(
    messages: list[dict],
) -> str:
    
    response = httpx.post(
        OLLAMA_URL,
        json={
          "model": OLLAMA_MODEL,
          "messages": messages,
          "stream": False,  
        },
        timeout=300.0
    )
    
    response.raise_for_status()
    
    data = response.json()
    
    return data["message"]["content"]


