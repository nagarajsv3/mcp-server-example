from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("LocalNotes")
NOTES_FILE = Path(__file__).resolve().parent / 'notes.txt'

@mcp.tool()
def add_note_to_file(content: str) -> str:
    """
    Appends the given content to a user's local notes file.

    Args:
        content: The text content to append.

    Returns:
        A success message indicating the file written to, or an error message.
    """
    try:
        NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(NOTES_FILE, 'a', encoding='utf-8') as f:
            f.write(content + "\n")
        return f'Content appended to {f}'
    except Exception as e:
        return f'Error appending to {f}: {e}'

@mcp.tool()
def read_note() -> str:
    """
    Reads and returns the contents of the user's local notes file.

    Returns:
        The full contents of `notes.txt`, or a message if the file is missing or empty.
    """

    try:
        if not NOTES_FILE.exists():
            return f"No notes file found at {str(NOTES_FILE)}."
        content = NOTES_FILE.read_text(encoding='utf-8').strip()
        if not content:
            return f"No notes found in {str(NOTES_FILE)}."
        return content
    except FileNotFoundError:
        return f"No notes file found at {str(NOTES_FILE)}."
    except Exception as e:
        return f"Error reading file {str(NOTES_FILE)}: {e}"

@mcp.tool()
def get_note_file_location() -> str:
    """
    Returns the absolute path to the local notes file.

    Returns:
        The absolute filesystem path to `notes.txt`, or an error message.
    """
    try:
        return str(NOTES_FILE.resolve())
    except Exception as e:
        return f"Error resolving path for {str(NOTES_FILE)}: {e}"

if __name__ == "__main__":
    print('starting to run')
    mcp.run()