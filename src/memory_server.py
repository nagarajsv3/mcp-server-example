# File: `src/websearch.py`
import os
import json
from typing import Optional, Any, Dict
from openai import OpenAI

import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()
import tempfile

client = OpenAI()
VECTOR_STORE_NAME = "MEMORIES"

mcp = FastMCP("Memories")

def get_or_create_vector_store() -> Any:
    """
    Try to find existing vector store, else create a new one.

    Returns:
        The vector store object
    """
    try:
        # Try to find existing vector store
        stores = client.vector_stores.list()
        for store in stores:
            if store.name == VECTOR_STORE_NAME:
                print(f"Found existing vector store: {VECTOR_STORE_NAME}")
                return store
        # Create new vector store if not found
        print(f"Creating new vector store: {VECTOR_STORE_NAME}")
        return client.vector_stores.create(name=VECTOR_STORE_NAME)
    except Exception as e:
        print(f"Error in get_or_create_vector_store: {e}")
        raise

@mcp.tool()
def save_memory(memory: str) -> Dict[str, Any]:
    """
    Save a memory string to the vector store.

    Args:
        memory: The memory string to save

    Returns:
        Dictionary with status and vector store id
    """
    try:
        # Get or create vector store
        vector_store = get_or_create_vector_store()

        # Save memory to a temp file for upload
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as f:
            f.write(memory)
            f.flush()

            # Upload file to vector store and poll for completion
            client.vector_stores.files.upload_and_poll(
                vector_store_id=vector_store.id,
                file=open(f.name, "rb")
            )

        print(f"Memory saved to vector store: {vector_store.id}")
        return {
            "status": "saved",
            "vector_store_id": vector_store.id
        }

    except Exception as e:
        print(f"Error saving memory: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

@mcp.tool()
def search_memory(query: str) -> Dict[str, Any]:
    """Search memories in the vector store and return relevant chunks"""
    try:
        vector_store = get_or_create_vector_store()

        results = client.vector_stores.search(
            vector_store_id=vector_store.id,
            query=query
        )

        context_texts = [
            content.text
            for item in results.data
            for content in item.content
            if content.type == "text"
        ]

        return {"results" : context_texts}

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
    
if __name__ == "__main__":
    # Optionally set log level via MCP_LOG_LEVEL env var if supported by FastMCP
    mcp.run(transport="stdio")

