from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from eligibility import check_basic_eligibility
from rag import search_documents
from llm import generate_answer


app = FastAPI(
    title="AI Government Scheme & Legal Rights Assistant",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():

    return {
        "project": "AI-Powered Government Scheme & Legal Rights Assistant",
        "status": "Backend is running",
        "features": [
            "AI Assistant",
            "RAG Search",
            "Government Knowledge Base",
            "Eligibility Engine",
            "Official Sources"
        ]
    }


@app.post("/api/search")
def search(query: str):

    results = search_documents(
        query,
        top_k=5
    )

    return {
        "query": query,
        "results": results
    }


@app.post("/api/ask")
def ask(query: str):

    results = search_documents(
        query,
        top_k=5
    )

    context_parts = []

    sources = []

    for result in results:

        text = result.get(
            "text",
            ""
        )

        metadata = result.get(
            "metadata",
            {}
        )

        context_parts.append(text)

        sources.append({
            "document": metadata.get(
                "document"
            ),
            "page": metadata.get(
                "page"
            ),
            "source_type": metadata.get(
                "source_type"
            )
        })

    context = "\n\n".join(
        context_parts
    )

    answer = generate_answer(
        query,
        context
    )

    return {
        "query": query,
        "answer": answer,
        "sources": sources
    }


@app.post("/api/eligibility")
def eligibility(profile: dict):

    schemes = profile.get(
        "schemes",
        []
    )

    user_profile = profile.get(
        "profile",
        {}
    )

    results = []

    for scheme in schemes:

        result = check_basic_eligibility(
            user_profile,
            scheme
        )

        results.append(result)

    return {
        "profile": user_profile,
        "results": results
    }
