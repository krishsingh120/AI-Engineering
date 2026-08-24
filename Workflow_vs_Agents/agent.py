import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


def add_numbers(a: float, b: float) -> float:
    """Adds two floating-point numbers together."""
    return a + b


def multiply_numbers(a: float, b: float) -> float:
    """Multiplies two floating-point numbers together."""
    return a * b
  


tools_map = {
    "add_numbers": add_numbers,
    "multiply_numbers": multiply_numbers,
}



def run_agent(user_prompt: str):
    print(f"User: {user_prompt}\n")

    # 3. Configure the Agent's tools and instructions
    config = types.GenerateContentConfig(
        system_instruction="You are a helpful calculation assistant. Always use your provided tools",
        tools=[add_numbers, multiply_numbers],
        temperature=0.0,
        automatic_function_calling={
            "disable": True
        }
    )

    chat = client.chats.create(
        model="gemini-3-flash-preview",
        config=config
    )

    response = chat.send_message(user_prompt)

    while response.function_calls:
        for function_call in response.function_calls:
            name = function_call.name
            args = function_call.args

            print(
                f"🤖 [Agent Decision]: Needs to call function "
                f"'{name}' with arguments {args}"
            )

            # Execute the local Python function dynamically
            if name in tools_map:
                tool_result = tools_map[name](**args)
                print(
                    f"🛠️ [Tool Output]: Result from {name} = "
                    f"{tool_result}\n"
                )
            else:
                tool_result = f"Error: Tool {name} not found."

            # Feed the tool execution results back into the chat session
            response = chat.send_message(
                types.Part.from_function_response(
                    name=name,
                    response={"result": tool_result}
                )
            )

    # Print the final compiled response once the agent completes its work
    print(f"🤖 Final Agent Answer: {response.text}")