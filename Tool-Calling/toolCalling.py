from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.tools import tool


import datetime
from articles import ARTICLE_DB_RESULTS


@tool
def get_top_article_by_view(number_of_articles: int) -> list:
    """Get the top article by views. Return top `number_of_articles` articles"""
    top_articles = sorted(
        ARTICLE_DB_RESULTS,
        key=lambda x: x["views"],
        reverse=True
    )

    return top_articles[:number_of_articles]


@tool
def get_top_article_by_likes(number_of_articles: int) -> list:
    """Get the top article by likes. Return top `number_of_articles` articles"""
    top_articles = sorted(
        ARTICLE_DB_RESULTS,
        key=lambda x: x["likes"],
        reverse=True
    )

    return top_articles[:number_of_articles]


@tool
def get_most_recent_articles(number_of_articles: int) -> list:
    """Get the most recent articles. Return top `number_of_articles` articles"""
    top_articles = sorted(
        ARTICLE_DB_RESULTS,
        key=lambda x: x["published_date"],
        reverse=True
    )

    return top_articles[:number_of_articles]


@tool
def get_all_articles() -> list:
    """Get all articles."""
    return ARTICLE_DB_RESULTS




def execute_tool_calls(tool_calls: list) -> list:
    result = []

    for tool_call in tool_calls:
        print(f'Executing Tool call: {tool_call["name"]}')
        print(f'Arguments: {tool_call["args"]}')

        if tool_call['name'] == 'get_top_article_by_view':
            result.append({
                'name': tool_call['name'],
                'result': get_top_article_by_view.invoke(tool_call['args'])
            })

        if tool_call['name'] == 'get_top_article_by_likes':
            result.append({
                'name': tool_call['name'],
                'result': get_top_article_by_likes.invoke(tool_call['args'])
            })

        if tool_call['name'] == 'get_most_recent_articles':
            result.append({
                'name': tool_call['name'],
                'result': get_most_recent_articles.invoke(tool_call['args'])
            })

        if tool_call['name'] == 'get_all_articles':
            result.append({
                'name': tool_call['name'],
                'result': get_all_articles.invoke(tool_call['args'])
            })

    return result



def initiate_the_agent(query, debug_mode=False) -> list:
    """Initiate the agent with the given query."""
    load_dotenv()

    tools = [
        get_top_article_by_view,
        get_top_article_by_likes,
        get_most_recent_articles,
        get_all_articles
    ]

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)
    llm_with_tools = llm.bind_tools(tools)

    response = llm_with_tools.invoke(query)

    if debug_mode:
        print(response.tool_calls)

    return execute_tool_calls(response.tool_calls)


# query1: "Can you give me top 3 most liked and viewed articles?"
# query2: "Can you give me top 5 most recent articles?"

response = initiate_the_agent("Can you give me top 5 most recent articles?", True)
response