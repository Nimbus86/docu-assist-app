# app/groq_client.py
import os, asyncio, httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.ai/v1")

_client = httpx.AsyncClient(timeout=60.0)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8),
       retry=retry_if_exception_type((httpx.HTTPError, asyncio.TimeoutError)))
async def call_groq(prompt: str, max_tokens: int = 800, temperature: float = 0.0) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-70b",
        "input": prompt,
        "max_output_tokens": max_tokens,
        "temperature": temperature
    }
    url = f"{GROQ_API_URL}/models/generate"
    resp = await _client.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data.get("output", "") or data.get("generated_text", "") or ""
