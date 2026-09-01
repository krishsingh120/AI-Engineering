from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing import Annotated
from typing_extensions import TypedDict
from operator import add
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()


class SharedState(TypedDict):
    dsa_topics: list[str]
    system_design_topics: list[str]


def parse_model_response(response):
    """Parse the model response"""
    return [topic.strip() for topic in response.split(",") if topic.strip()]


def find_relevant_dsa_topics(shared_state: SharedState) -> SharedState:
    """Find relevant DSA topics for year 2025."""
    query = """
    Can you provide top 5 DSA topics to master for Software Engineering interviews in 2025?.
    Please only return the DSA topics comma separated, no other detail is needed. 
    """
    model = ChatOpenAI(model="gpt-4o")

    response = model.invoke(query)
    # shared_state["dsa_topics"] = parse_model_response(response.content)

    return {
        "dsa_topics": parse_model_response(response.content),
        "system_design_topics": [],
    }


def find_relevant_system_design_topics(shared_state: SharedState) -> SharedState:
    """Find relevant System Design topics for year 2025."""
    query = """
    Can you provide top 5 System Design topics to master for Software Engineering interviews in 2025?.
    Please only return the System Design topics comma separated, no other detail is needed. 
    """
    model = ChatOpenAI(model="gpt-4o")

    response = model.invoke(query)
    shared_state["system_design_topics"] = parse_model_response(response.content)

    return shared_state


def build_graph():
    # Building a Graph
    # State of the Graph that will be shared among nodes.
    workflow = StateGraph(SharedState)

    # Add nodes.
    workflow.add_node("find_relevant_dsa_topics", find_relevant_dsa_topics)
    workflow.add_node(
        "find_relevant_system_design_topics", find_relevant_system_design_topics
    )

    # Define the edges of the graph.
    workflow.add_edge(START, "find_relevant_dsa_topics")
    workflow.add_edge("find_relevant_dsa_topics", "find_relevant_system_design_topics")
    workflow.add_edge("find_relevant_system_design_topics", END)

    checkpointer = InMemorySaver()
    graph = workflow.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "1"}}
    response = graph.invoke({}, config)

    # print(graph.get_graph().draw_mermaid())

    return response, graph, config



response, graph, config = build_graph()
print(response)
snapshots = list(graph.get_state_history(config))
print(snapshots[1])


list.reverse(snapshots)

for snapshot in snapshots:
    print("================== Snapshot details: ==================")
    print(snapshot.values)
    print(snapshot.next)
    print("\n\n")