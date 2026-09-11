from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint,
    HuggingFacePipeline,
)

db = SQLDatabase.from_uri("sqlite:///Chinook.db", sample_rows_in_table_info=0)


def get_schema(_):
    return db.get_table_info()


def run_query(query):
    print(f"Query being run: {query} \n\n")
    return db.run(query)


print(get_schema(""))


def get_llm(load_from_hugging_face=False):
    if load_from_hugging_face:
        llm = HuggingFaceEndpoint(
            repo_id="Qwen/Qwen2.5-VL-7B-Instruct",
            task="text-generation",
            provider="hyperbolic",  # set your provider here
        )

        return ChatHuggingFace(llm=llm)

    return ChatOpenAI(model="gpt-4", temperature=0.0)


def write_sql_query(llm):
    template = """Based on the table schema below, write a SQL query that would answer the user's question:
    {schema}

    Question: {question}
    SQL Query:"""

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Given an input question, convert it to a SQL query. No pre-amble. "
                "Please do not return anything else apart from the SQL query, no prefix aur suffix quotes, no sql keyword, nothing please",
            ),
            ("human", template),
        ]
    )

    return (
        RunnablePassthrough.assign(schema=get_schema) | prompt | llm | StrOutputParser()
    )


def answer_user_query(query, llm):
    template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
    {schema}

    Question: {question}
    SQL Query: {query}
    SQL Response: {response}"""

    prompt_response = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Given an input question and SQL response, convert it to a natural language answer. No pre-amble.",
            ),
            ("human", template),
        ]
    )

    full_chain = (
        RunnablePassthrough.assign(query=write_sql_query(llm))
        | RunnablePassthrough.assign(
            schema=get_schema,
            response=lambda x: run_query(x["query"]),
        )
        | prompt_response
        | llm
    )

    return full_chain.invoke({"question": query})



# Query types to try out:

# 1. Straight forward queries: Give me the name of 10 Artists
# 2. Querying for multiple columns: Give me the name and artist ID of 10 Artists
# 3. Querying a table by a foreign key: Give me 10 Albums by the Artist with ID 1
# 4. Joining with a different table: Give some Albums by the Artist name Audioslave'
# 5. Multi-level Joins: Give some Tracks by the Artist name Audioslave'


load_dotenv()

# write_sql_query(llm=get_llm(load_from_hugging_face=True)).invoke({"question": "Give me 10 Artists"})
query = 'Give some Tracks by the Artist name Audioslave'
response = answer_user_query(query, llm=get_llm(load_from_hugging_face=False))
print(response.content)



# query = '''
# SELECT T.Name
# FROM Track T
# WHERE T.AlbumId IN (
#     SELECT A.AlbumId
#     FROM Album A
#     LEFT JOIN Artist Ar ON A.ArtistId = Ar.ArtistId
#     WHERE Ar.Name = "Audioslave"
# );
# '''
# query = 'SELECT Album.* FROM Album LEFT JOIN Artist ON Album.ArtistId = Artist.ArtistId WHERE Artist.Name = "Audioslave" LIMIT 10'
query = '''
SELECT Track.Name 
FROM Track 
JOIN Album ON Track.AlbumId = Album.AlbumId 
JOIN Artist ON Album.ArtistId = Artist.ArtistId 
WHERE Artist.Name = 'Audioslave' 
'''
response = run_query(query)
print(response)