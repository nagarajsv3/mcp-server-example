from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Prompt")

@mcp.prompt()
def get_user_prompt(topic: str) -> str:
    """
    Returns a prompt that will do detailed analysis on the topic.

    Args:
        topic: The topic to search and analyze

    Returns:
        A formatted prompt string requesting detailed analysis of the specified topic
    """
    return f"Please do the detailed analysis on the topic {topic}"

if __name__ == "__main__":
    mcp.run()