import os

from IPython.display import Markdown, display
from agent_framework.a2a import A2AAgent
from dotenv import load_dotenv

host = "localhost"
port = 9999
base_url = f"http://{host}:{port}"
# Create A2A agent with direct URL configuration
chat_agent = A2AAgent(
    name="ChatAgent",
    url=base_url,
)


async def callFunc():
    prompt = "What are some well known AI Engineering design patterns?"
    response = await chat_agent.run(prompt)

    return response


response = callFunc()

display(Markdown(response.text))
