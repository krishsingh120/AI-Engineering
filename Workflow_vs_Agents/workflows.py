from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


class WorkflowState(TypedDict):
    query: str
    category: str
    response: str


class CategoryClassification(BaseModel):
    category: Literal["billing", "technical"] = Field(
        description="Classify the intent into 'billing' (payments, refunds, pricing) or 'technical' (bugs, uptime, API errors, accounts)."
    )


def classifier_node(state: WorkflowState):
    print("--- [Node] Classifying Query ---")
    user_query = state["query"].lower()

    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=0
    )

    structured_llm = llm.with_structured_output(CategoryClassification)

    # 2. Build the system prompt instruction template
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an automated routing assistant. Analyze the incoming user inquiry and classify its department destination."
        ),
        ("human", "{user_query}")
    ])

    # 3. Chain and execute
    classification_chain = prompt | structured_llm
    prediction = classification_chain.invoke({"user_query": user_query})

    # Return the clean, validated field to update the graph state
    return {"category": prediction.category}


def billing_expert_node(state: WorkflowState):
    print("--- [Node] Processing Billing Ticket ---")
    return {
        "response": "Routing your inquiry directly to our billing and payment operations team."
    }


def technical_expert_node(state: WorkflowState):
    print("--- [Node] Processing Technical Ticket ---")
    return {
        "response": "Opening a high-priority ticket with engineering to troubleshoot your system."
    }


def router_logic(state: WorkflowState) -> Literal["to_billing", "to_technical"]:
    if state["category"] == "billing":
        return "to_billing"
    return "to_technical"


builder = StateGraph(WorkflowState)

builder.add_node("classifier", classifier_node)
builder.add_node("billing_processor", billing_expert_node)
builder.add_node("technical_processor", technical_expert_node)

builder.add_edge(START, "classifier")

builder.add_conditional_edges(
    "classifier",
    router_logic,
    {
        "to_billing": "billing_processor",
        "to_technical": "technical_processor"
    }
)

builder.add_edge("billing_processor", END)
builder.add_edge("technical_processor", END)

graph = builder.compile()



input_state_1 = {"query": "I need help with my monthly invoice payment"}
result_1 = graph.invoke(input_state_1)

print(f"Result 1 Category: {result_1['category']}")
print(f"Result 1 Response: {result_1['response']}\n")


input_state_2 = {"query": "The API keeps returning a 500 error code"}
result_2 = graph.invoke(input_state_2)

print(f"Result 2 Category: {result_2['category']}")
print(f"Result 2 Response: {result_2['response']}")



from IPython.display import Image, display

try:
    # Fetch the graph architecture and render it as PNG bytes
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception as e:
    print(f"Could not render image. Ensure your environment supports it: {e}")