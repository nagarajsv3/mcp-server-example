# File: `src/websearch.py`
import os
import json
from typing import Optional
from openai import OpenAI

import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("WebSearch")

@mcp.tool(
    name="websearch",
    description="Search the web using OpenAI ChatGPT and return a concise summary."
)
def websearch(query: str) -> str:
    """Search the user query string using openai api.

     Parameters
     ----------
     query : str
         search against openai using this query

     Returns
     -------
     str
         A human-readable message:
         - On success: "The response retrieved from openai"
    """
    if not query or not isinstance(query, str):
        return "Invalid search query."

    # Prefer OPENAI_API_KEY; allow PERPLEXITY_API_KEY as a fallback if you reused env var
#    key = os.getenv("OPENAI_API_KEY") or os.getenv("PERPLEXITY_API_KEY")
    key = os.getenv("OPENAI_API_KEY")

    if not key:
        return "Missing API key. Set OPENAI_API_KEY (or PERPLEXITY_API_KEY) in the environment."

    messages = [{"role": "user", "content": f"Search and summarize: {query}"}]
    model = os.getenv("CHAT_MODEL", "gpt-4.1-mini")
    max_tokens = int(os.getenv("CHAT_MAX_TOKENS", "400"))

    # Try official OpenAI client (dynamic import)
    try:
        if OpenAI:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            resp = client.chat.completions.create(model=model, messages=messages, max_tokens=max_tokens)
            content: Optional[str] = None
            if hasattr(resp, "choices") and resp.choices:
                first = resp.choices[0]
                content = getattr(getattr(first, "message", None), "content", None) or getattr(first, "text", None)
            if content:
                return content.strip()
    except Exception:
        # Fall through to HTTP fallback
        pass

    # HTTP fallback to OpenAI API
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {"model": model, "messages": messages, "max_tokens": max_tokens}
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        r.raise_for_status()
        data = r.json()
        choice = data.get("choices", [{}])[0]
        msg = (choice.get("message") or {}).get("content") or choice.get("text")
        if msg:
            return msg.strip()
        return f"No usable completion returned for query: {query}"
    except requests.exceptions.RequestException as e:
        return f"Network error while contacting OpenAI: {e}"
    except ValueError:
        return "Invalid JSON response from OpenAI."
    except Exception as e:
        return f"Unexpected error: {e}"


@mcp.tool()
def health() -> str:
    """Simple health-check tool."""
    return "ok"


if __name__ == "__main__":
    # Optionally set log level via MCP_LOG_LEVEL env var if supported by FastMCP
    mcp.run()
    # res = websearch(query='hi')
    # print(res)
