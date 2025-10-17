# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
from prometheus_client import Counter, generate_latest
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")  # Look for .env in parent directory
load_dotenv()  # Also check current directory

# Set your OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY", "your-api-key")

# Debug: Print first few characters of API key (for verification)
api_key = os.getenv("OPENAI_API_KEY", "not-found")
print(f"API Key loaded: {api_key[:10]}..." if len(api_key) > 10 else f"API Key: {api_key}")

# Initialize OpenAI client
client = openai.OpenAI(api_key=openai.api_key)

# FastAPI app
app = FastAPI()

# Prometheus metrics
token_counter_total = Counter("llm_tokens_total", "Total tokens used", ["model"])
token_counter_prompt = Counter("llm_tokens_prompt", "Prompt tokens used", ["model"])
token_counter_completion = Counter("llm_tokens_completion", "Completion tokens used", ["model"])

class PromptRequest(BaseModel):
    prompt: str
    model: str = "gpt-4.1"

@app.post("/chat")
async def chat(request: PromptRequest):
    response = client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": request.prompt}],
    )
    
    usage = response.usage
    
    # Update Prometheus metrics
    token_counter_prompt.labels(model=request.model).inc(usage.prompt_tokens)
    token_counter_completion.labels(model=request.model).inc(usage.completion_tokens)
    token_counter_total.labels(model=request.model).inc(usage.total_tokens)
    
    return {
        "response": response.choices[0].message.content,
        "usage": {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens
        }
    }

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return generate_latest()