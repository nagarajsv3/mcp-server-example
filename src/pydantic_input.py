from pydantic import BaseModel, Field
from typing import List, Dict

from mcp.server.fastmcp import FastMCP

class Person(BaseModel):
    first_name : str = Field(... , description="First Name")
    last_name : str = Field(... , description="Last Name")
    experience : int = Field(... , description="Experience")
    previous_addresses : List[str] = Field(default_factory=list, description="List of previous addresses")

mcp = FastMCP("Pydantic Inputs")

@mcp.tool()
def add_person_to_member_database(person: Person) -> str:
    """
    Adds person data to member database.

    Args:
        person (Person): An instance of the Person class containing the following personal details:
            - first_name (str): The person's given name.
            - last_name (str): The person's family name.
            - experience (int): Number of years of experience.
            - previous_addresses (List[str]): A list of the person's previous residential addresses.

    Returns:
        str: A confirmation message indicating that the data has been logged.
    """
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"First Name: {person.first_name}\n")
        log_file.write(f"Last Name: {person.last_name}\n")
        log_file.write(f"Years of Experience: {person.experience}\n")
        log_file.write(f"Previous Addresses:\n")

        for idx, address in enumerate(person.previous_addresses, 1):
            log_file.write(f"  ({idx}). {address}\n")

        log_file.write("\n")

    return "Data has been logged"


if __name__ == "__main__":
    # Optionally set log level via MCP_LOG_LEVEL env var if supported by FastMCP
    mcp.run()
    # res = websearch(query='hi')
    # print(res)
