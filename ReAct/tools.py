import requests
import math


class ToolRegistry:

    def __init__(self):
        self.tools = {
            "search": self.search,
            "calculator": self.calculator
        }

    def execute(self, tool_name, tool_input):

        if tool_name not in self.tools:
            available = ", ".join(self.tools.keys())
            return f"Error: Tool '{tool_name}' not found. Available tools: {available}"

        try:
            return self.tools[tool_name](tool_input)
        except Exception as e:
            return f"Tool execution error: {str(e)}"


    def search(self, query):

        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1
        }

        try:
            response = requests.get(url, params=params).json()

            if response.get("AbstractText"):
                return response["AbstractText"]

            elif response.get("RelatedTopics"):
                topics = response["RelatedTopics"]
                if len(topics) > 0 and "Text" in topics[0]:
                    return topics[0]["Text"]

            return "No relevant results found."

        except Exception as e:
            return f"Search error: {str(e)}"

    def calculator(self, expression):
        try:
            return str(eval(expression, {"__builtins__": {}}, {"sqrt": math.sqrt}))
        except Exception as e:
            return f"Calculation error: {str(e)}"