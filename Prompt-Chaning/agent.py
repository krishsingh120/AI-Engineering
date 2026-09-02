from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph, START
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv


class SharedState(TypedDict):
    query: str
    model: ChatOpenAI
    from_ml_topic: bool
    ai_answer: str


class GraderOutput(TypedDict):
    from_machine_learning_topic: bool


def build_model(shared_state: SharedState):
    model = ChatOpenAI(model="gpt-4o-mini")
    shared_state["model"] = model
    return shared_state


def get_query_topic(shared_state: SharedState):
    print("Determining if the query is related to machine learning topics...")

    prompt = """
You are a classifier that determines if a user's query is related to machine learning topics.
Given the user's query, return True if it is related to machine learning topics, otherwise return False.
    """

    model = shared_state["model"]
    structured_llm_grader = model.with_structured_output(GraderOutput)
    query = shared_state["query"]

    grade_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt),
            ("human", "User's Query: \n\n {query}"),
        ]
    )

    retrieval_grader = grade_prompt | structured_llm_grader

    result = retrieval_grader.invoke({"query": query})
    shared_state["from_ml_topic"] = result["from_machine_learning_topic"]

    return shared_state


def grader_node(shared_state: SharedState):
    if shared_state["from_ml_topic"]:
        return "continue"

    return "exit"


def answer_query(shared_state: SharedState):
    print("Answering the user's query...")
    prompt = """
You are an expert in machine learning. Answer the user's query under 200 words.
    """
    model = shared_state["model"]
    query = shared_state["query"]
    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt),
            ("human", "User's Query: \n\n {query}"),
        ]
    )
    answer_chain = answer_prompt | model | StrOutputParser()
    result = answer_chain.invoke({"query": query})
    shared_state["ai_answer"] = result

    return shared_state


def build_graph():
    workflow = StateGraph(SharedState)

    # Add Nodes
    workflow.add_node(build_model, "build_model")
    workflow.add_node(get_query_topic, "get_query_topic")
    workflow.add_node(answer_query, "answer_query")

    workflow.add_edge(START, "build_model")
    workflow.add_edge("build_model", "get_query_topic")
    workflow.add_conditional_edges(
        "get_query_topic", grader_node, {"continue": "answer_query", "exit": END}
    )
    workflow.add_edge("answer_query", END)

    return workflow.compile()


# Query 1: "What are the latest advancements in machine learning?"
# Query 2: "What is the capital of India?"
def execute_prompt_chain_workflow():
    workflow = build_graph()
    initial_state: SharedState = {
        "query": "What is the capital of India?",
    }

    agent_response = workflow.invoke(initial_state)
    print(agent_response)

    if agent_response["from_ml_topic"]:
        print("AI's Answer:", agent_response["ai_answer"])
    else:
        print("The query is not related to machine learning topics.")


load_dotenv()
execute_prompt_chain_workflow()
