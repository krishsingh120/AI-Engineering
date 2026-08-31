from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


model = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are a helpful assistant. Answer all questions to the best of your ability."
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | model


ai_msg = chain.invoke(
    {
        "messages": [
            HumanMessage(content="Can you explain Dynamic Programming under 50 words?")
        ],
    }
)

print(ai_msg.content)


## Method 1: Pass Chat History to your LLM as a context.

chat_history = [
    HumanMessage(content="Can you explain Dynamic Programming under 50 words?"),
    AIMessage(content=ai_msg.content),
]

chat_history


def interrogate_model(chat_history: list, preserve_chat_history=True):
    current_message = [HumanMessage(content="What did I ask you earlier?")]
    chat_messages = []

    if preserve_chat_history:
        chat_messages = chat_history + current_message
    else:
        chat_messages = current_message

    ai_msg = chain.invoke({"messages": chat_messages})

    return ai_msg.content


interrogate_model(chat_history, preserve_chat_history=True)


# Method 2: Summarize the chat history


def summarize_chat_history(chat_history: list):
    """Summarizes the chat history when the message count is greater than 4."""

    if len(chat_history) >= 4:
        summary_prompt = (
            "Distill the above chat messages into a single summary message. "
            "Include as many specific details as you can."
        )
        print(chat_history)
        summary_message = chain.invoke(
            chat_history + [HumanMessage(content=summary_prompt)]
        )

        return summary_message.content

    return ""


def interrogate_model_with_summary(query: str, chat_history: list, debug_mode=False):
    current_message = [HumanMessage(content=query)]
    chat_messages = []

    if len(chat_history) >= 4:
        print("Summarizing your content...")
        summary_message = summarize_chat_history(chat_history)
        chat_messages = [AIMessage(content=summary_message)] + current_message
    else:
        chat_messages = chat_history + current_message

    if debug_mode:
        print("Messages sent to the model:")
        print(chat_messages, "\n")

    ai_msg = chain.invoke({"messages": chat_messages})

    return AIMessage(content=ai_msg.content)


def chat_with_model(query: str, chat_history: list, debug_mode=False):
    query_response = interrogate_model_with_summary(query, chat_history, debug_mode)

    # Append the query and response to the chat history
    chat_history.append(HumanMessage(content=query))
    chat_history.append(query_response)

    return query_response, chat_history


chat_history = []

query1 = "Can you explain Dynamic Programming under 50 words?"
query_response1, chat_history = chat_with_model(query1, chat_history, debug_mode=True)

print(query_response1.content)


query2 = "Can you explain Graph data structures under 50 words?"
query_response2, chat_history = chat_with_model(query2, chat_history, debug_mode=True)

print(query_response2.content)


query3 = "Can you tell me what did I ask till now?"
query_response3, chat_history = chat_with_model(query3, chat_history, debug_mode=True)

print(query_response3.content)
