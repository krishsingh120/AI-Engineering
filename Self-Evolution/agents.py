from langchain_google_genai import ChatGoogleGenerativeAI
from concurrent.futures import ThreadPoolExecutor
from langchain_tavily import TavilySearch
from dotenv import load_dotenv


def generate_answer(
    search_query: str,
    web_results: str,
    environment_feedback: str,
    model: ChatGoogleGenerativeAI,
) -> str:
    print("Generating answer...")
    prompt = """
        Given the search query, web results and environment feedback, provide a concise and accurate answer.
        
        1. Search Query: {search_query}
        2. Web Results: {web_results}
        3. Environment Feedback: {environment_feedback}

        Focus on Facts: Prioritize numbers, dates, definitions, and distinct arguments.
        If environment feedback is provided, incorporate it into the answer.
        """

    return model.invoke(
        prompt.format(
            search_query=search_query,
            web_results=web_results,
            environment_feedback=environment_feedback,
        )
    ).content


def web_search(query: str) -> str:
    """Perform a web search and return the results"""
    print("Performing Web Search...")

    web_search_tool = TavilySearch(max_results=20)
    web_results = web_search_tool.invoke({"query": query})

    return _parse_web_search_results(web_results)


def _parse_web_search_results(web_search_result) -> str:
    """Parse the web search results and filter based on relevance score"""

    if not web_search_result or "results" not in web_search_result:
        return ""

    search_answers = []
    for result in web_search_result["results"]:
        search_content = result["content"]
        search_answers.append(search_content)

    return "\n".join(search_answers)


def get_environment_feedback(answer: str, search_query: str, web_results: str) -> str:
    print("Generating Environment Feedback...")
    prompt = """
        Given the answer, search query, and web results, provide feedback on the answer provided for the search query.
        Keep the feedback concise and focused on factual accuracy.
        Take the Web Results as a source of truth when evaluating the answer.
        
        1. Answer: {answer}
        2. Search Query: {search_query}
        3. Web Results: {web_results}
        """
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
    )

    return model.invoke(
        prompt.format(answer=answer, search_query=search_query, web_results=web_results)
    ).content


MAX_REFINEMENTS = 3


def start_self_evolution(model: ChatGoogleGenerativeAI, search_query: str):
    refinement_count = 0
    answer = ""
    environment_feedback = ""
    web_results = web_search(search_query)

    while refinement_count < MAX_REFINEMENTS:
        print(f"Refinement Iteration: {refinement_count + 1}")
        answer = generate_answer(search_query, web_results, environment_feedback, model)
        environment_feedback = get_environment_feedback(
            answer, search_query, web_results
        )
        refinement_count += 1

    return answer


def candidates_crossover(evolved_answers: list[str], search_query: str) -> str:
    """Combine multiple evolved answers into a single answer"""
    print("Performing Crossover of Candidates...")
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    prompt = """
        Your task is to research a topic and try to fulfill the user query in the <user> tags.
        <instructions>
        You are given a list of candidate answers in <answer_list> tags below. Combine them into a single answer so that,
        + it best fulfills the initial user query in the <user> tags.
        + If there are conflicting information, try to reconcile them in a logically sound way.
        </instructions>
        Here is the user query.
        <user>
        {query}
        </user>
        Here is the list of candidate answers you need to merge.
        <answer_list>
        {answer_list}
        </answer_list>
        Only output a combined answer from the answers in <answer_list>. Do NOT use other information.
        """

    return model.invoke(
        prompt.format(
            query=search_query,
            answer_list="\n".join(
                [
                    f"Candidate Answer: {evolved_answer}"
                    for evolved_answer in evolved_answers
                ]
            ),
        )
    ).content


CANDIDATES = 3
CANDIDATES_CONFIGURATION = [
    {
        "top_k": 30,
        "temperature": 0.5,
    },
    {
        "top_k": 40,
        "temperature": 1.0,
    },
    {
        "top_k": 50,
        "temperature": 1.5,
    },
]


def perform_self_evolution(search_query: str):
    evolved_answers = []
    for index, candidate_config in enumerate(CANDIDATES_CONFIGURATION):
        print(f"\n Spawning Candidate: {index + 1} \n")
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=candidate_config["temperature"],
            top_k=candidate_config["top_k"],
        )
        evolved_answer = start_self_evolution(model, search_query)
        evolved_answers.append(evolved_answer)

    return candidates_crossover(evolved_answers, search_query)


load_dotenv()
query = "What are the investment philosophies of Duan Yongping, Warren Buffett, and Charlie Munger?"
crossover_evolved_answer = perform_self_evolution(query)
print("\n Final Evolved Answer after Crossover: \n")
print(crossover_evolved_answer)


def perform_self_evolution_in_parallel(search_query: str):
    future_responses = []
    evolved_answers = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        for index, candidate_config in enumerate(CANDIDATES_CONFIGURATION):
            print(f"\n Spawning Candidate: {index + 1} \n")
            model = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=candidate_config["temperature"],
                top_k=candidate_config["top_k"],
            )
            future_response = executor.submit(start_self_evolution, model, search_query)
            future_responses.append(future_response)

    evolved_answers = [future.result() for future in future_responses]
    return candidates_crossover(evolved_answers, search_query)


def search_without_self_evolution(search_query: str) -> str:
    web_results = web_search(search_query)
    model = ChatGoogleGenerativeAI(model="gemini-2.5-pro")
    answer = generate_answer(search_query, web_results, "", model)
    return answer


search_answer = search_without_self_evolution(query)
print("\n Search Answer without Self Evolution: \n")
print(search_answer)
