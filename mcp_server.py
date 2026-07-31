import json
from pathlib import Path
import requests

from fastmcp import FastMCP

DATA_FILE = Path(__file__).with_name("data.json")
mcp = FastMCP("items-server")


@mcp.tool()
def get_items() -> list[dict[str, object]]:
    try:
        response = requests.get("http://127.0.0.1:8000/items", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching items: {e}")
        with DATA_FILE.open("r", encoding="utf-8") as handle:
            return json.load(handle)


if __name__ == "__main__":
    mcp.run()
