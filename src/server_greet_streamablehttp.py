from mcp.server.fastmcp import FastMCP

mcp = FastMCP("greet")

@mcp.tool()
def greet(name : str) -> str:
    """
    Greets a user by name with a friendly message.
        Args:
            name (str): The name of the person to greet.
        Returns:
            A friendly greeting message addressed to the given name.
    """
    return f"Hi {name}. Hope you are doing good."

if __name__ == '__main__':
    mcp.run(transport="streamable-http")