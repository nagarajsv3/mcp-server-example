from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
def get_weather(location: str) -> str:
    """Return a short human-readable weather summary for a given location.

    Args:
        location (str): Location name (city, region, or coordinates) to query weather for.

    Returns:
        str: A brief weather summary for the specified location.
    """
    return "Weather is hot and dry"

if __name__ == "__main__":
    print('starting to run')
    mcp.run()