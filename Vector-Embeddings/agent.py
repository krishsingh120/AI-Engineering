from google.genai import types
from google import genai
from dotenv import load_dotenv

import numpy as np
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

client = genai.Client(
    api_key=API_KEY, http_options=types.HttpOptions(api_version="v1alpha")
)

word = "health care"

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=word,
)

word_embedding = response.embeddings[0].values

print(word_embedding[:20])


def calculate_cosine_similarity_numpy(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0  # Handle cases where one or both vectors are zero vectors

    return dot_product / (norm_vec1 * norm_vec2)


# word2 = "medical insurance"
word3 = "hospital care"

response2 = client.models.embed_content(
    model="gemini-embedding-001",
    contents=word3,
)

word_embedding2 = response2.embeddings[0].values


#  "medical insurance",  "health care" => 64.27%
#  "customer care",  "health care" => 57.45%
#  "hospital care",  "health care" => 69.05%
calculate_cosine_similarity_numpy(word_embedding, word_embedding2)
