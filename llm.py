import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_answer(question, context):

    prompt = f"""
You are an AI Government Scheme and Legal Rights Assistant.

Answer the user's question ONLY using the
government document context provided below.

Rules:

1. Do not invent facts.
2. Do not make assumptions.
3. If the answer is not available in the
   provided context, say that verified
   information was not found.
4. Give a simple and clear answer.
5. This is informational guidance, not legal advice.

User Question:
{question}

Government Document Context:
{context}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text
