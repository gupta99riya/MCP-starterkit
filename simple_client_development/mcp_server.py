import math
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool(description="Adds two integers and returns their sum.")
def add(a: int, b: int) -> int:
    print(f"Server received add request: {a}, {b}")
    return a + b

@mcp.tool(description="Multiplies two integers and returns the result.")
def multiply(a: int, b: int) -> int:
    print(f"Server received multiply request: {a}, {b}")
    return a * b

@mcp.tool(description="Calculates the sine of the given integer value (in radians).")
def sine(a: int) -> int:
    print(f"Server received sine request: {a}")
    return math.sin(a)

@mcp.tool(description="Fetches current weather for a given city using WeatherAPI.com.")
def get_weather(city: str) -> dict:
    print(f"Server received weather request: {city}")
    url = f"http://api.weatherapi.com/v1/current.json?key=f9f4f1972fbc4d769bf61758250708&q={city}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"Failed to fetch weather for {city}."}
    data = response.json()
    return {
        "city": data["location"]["name"],
        "region": data["location"]["region"],
        "country": data["location"]["country"],
        "temperature_C": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"]
    }

if __name__ == "__main__":
    print("Starting MCP Server....")
    mcp.run(transport="stdio")
