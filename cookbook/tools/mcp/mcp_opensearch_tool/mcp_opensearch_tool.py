from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools
from mcp.client.stdio import StdioServerParameters
from textwrap import dedent
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()  #Load from .env if exists

async def opensearch_mcp_agent():
    server_params = StdioServerParameters(
        command="python",
        args=["opensearch_mcp_server.py"],
        env={
            "OPENSEARCH_HOST": os.getenv("OPENSEARCH_HOST"),
            "OPENSEARCH_INDEX": os.getenv("OPENSEARCH_INDEX"),
            "OPENSEARCH_API_KEY": os.getenv("OPENSEARCH_API_KEY", "")
        }
    )

    async with MCPTools(server_params=server_params) as mcp_tools:
        agent = Agent(
            name="OpenSearch Agent",
            description="Stores and retrieves conversations from OpenSearch.",
            model=OpenAIChat(id="gpt-4o"),
            tools=[mcp_tools],
            instructions=dedent("""
                You are a smart assistant who logs all conversations in a searchable knowledge base (OpenSearch).
                Always:
                1. Format your response as JSON: {'user': <USER_QUERY>, 'assistant': <ASSISTANT_RESPONSE>}
                2. Call the tool 'push_to_opensearch' with this JSON.
            """),
            show_tool_calls=True,
        )
        return agent

async def main():
    agent = await opensearch_mcp_agent()
    res = await agent.arun("What is OpenSearch used for?")
    print(res.content)

if __name__ == "__main__":
    asyncio.run(main())
