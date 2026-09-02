from pydantic import BaseModel
from typing_extensions import Literal, TypedDict
from pydantic import Field
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph, START
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader

from dotenv import load_dotenv


class RouterOutput(TypedDict):
    output: Literal["github", "medium", "none"] = (
        Field(
            default="none",
            description="The output destination, either 'github' or 'medium'. If neither is suitable, use 'none'.",
        ),
    )
    user_handle: str = Field(
        default="none",
        description="The user's profile handle for the specified output destination.",
    )


class SharedState(TypedDict):
    query: str
    user_handle: str
    destination: Literal["github", "medium"]
    profile_summary: str
    model: ChatOpenAI


def build_model(shared_state: SharedState):
    shared_state["model"] = ChatOpenAI(model="gpt-4o", temperature=0)
    return shared_state


def router_agent(shared_state: SharedState):
    prompt = f"""
    You are an expert social media profile assistant. Based on the user's preference, you will determine whether to pull their GitHub or Medium profile details.
    
    Ensure your response is a valid JSON object matching the RouterOutput schema.
    """

    model_with_structured_output = shared_state["model"].with_structured_output(
        RouterOutput
    )
    grade_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt),
            ("human", "User's Query: \n\n {query}"),
        ]
    )

    retrieval_grader = grade_prompt | model_with_structured_output
    response = retrieval_grader.invoke({"query": shared_state["query"]})
    shared_state["destination"] = response["output"]
    shared_state["user_handle"] = response["user_handle"]

    return shared_state


load_dotenv()
shared_state = build_model(
    {
        "query": "Can you summarize medium profile of SauravP97",
    }
)
router_agent(shared_state)
print(shared_state["destination"], shared_state["user_handle"])


# Conditional edge function to route to the appropriate node
def route_destination(shared_state: SharedState):
    # Return the node name you want to visit next
    if shared_state["destination"] == "github":
        return "summarize_github_profile"
    elif shared_state["destination"] == "medium":
        return "summarize_medium_profile"
    else:
        return "end_node"


# Helper Functions
def read_github_profile(user_handle: str):
    """Reads the GitHub profile content for the given GitHub handle."""
    print("Reading GitHub profile content...")
    github_profile_url = "https://www.github.com/" + user_handle
    documents = WebBaseLoader(github_profile_url).load()
    page_content = ""

    for document in documents:
        page_content += document.page_content

    return page_content.strip()


def read_medium_profile(user_handle: str):
    """Reads the Medium profile content for the given Medium user handle."""
    print("Reading Medium profile content...")
    medium_profile_url = f"https://{user_handle}.medium.com"
    documents = WebBaseLoader(medium_profile_url).load()
    page_content = ""

    for document in documents:
        page_content += document.page_content

    return page_content.strip()


def build_graph():
    workflow = StateGraph(SharedState)

    # Add Nodes
    workflow.add_node(build_model, "build_model")
    workflow.add_node(router_agent, "router_agent")
    workflow.add_node(summarize_github_profile, "summarize_github_profile")
    workflow.add_node(summarize_medium_profile, "summarize_medium_profile")

    workflow.add_edge(START, "build_model")
    workflow.add_edge("build_model", "router_agent")
    workflow.add_conditional_edges(
        "router_agent",
        route_destination,
        {
            "summarize_github_profile": "summarize_github_profile",
            "summarize_medium_profile": "summarize_medium_profile",
            "end_node": END,
        },
    )
    workflow.add_edge("summarize_github_profile", END)
    workflow.add_edge("summarize_medium_profile", END)

    return workflow.compile()


load_dotenv()
compiled_graph = build_graph()
workflow_response: SharedState = compiled_graph.invoke(
    {"query": "Summarize the linkedin profile for user handle Saurav"}
)

print(f"\n Profile Type: {workflow_response['destination']}")
if workflow_response["destination"] != "none":
    print(f"\n\n Profile Summary: {workflow_response['profile_summary']}")
else:
    print("\n\n No suitable profile found.")
