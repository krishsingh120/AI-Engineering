# Create server parameters for stdio connection
from langchain_core.messages import AIMessage, HumanMessage, ToolCall
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()


# Layer 2: Middleware between MCP Servers and Agent
client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["./math.server.py"],
            "transport": "stdio",
        },
        # Add more MCP Servers here...
    }
)


async def callingcalling():
    tools = await client.get_tools()
    agent = create_react_agent("openai:gpt-4.1", tools)
    math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})


def parse_agent_response(response):
    for message in response["messages"]:
        if isinstance(message, HumanMessage):
            print(f"Human: {message.content}")
        if isinstance(message, AIMessage):
            if message.tool_calls:
                print(f"Tool Call: {message.tool_calls}")
            else:
                print(f"Agent: {message.content}")


parse_agent_response(math_response)


client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["./math.server.py"],
            "transport": "stdio",
        },
        "weather": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["./weather.server.py"],
            "transport": "stdio",
        },
        # Add more MCP Servers here...
    }
)


async def callcall():
    tools = await client.get_tools()
    agent = create_react_agent("openai:gpt-4.1", tools)
    agent_response = await agent.ainvoke(
        {"messages": "How's the weather in San Francisco"}
    )
    parse_agent_response(agent_response)
