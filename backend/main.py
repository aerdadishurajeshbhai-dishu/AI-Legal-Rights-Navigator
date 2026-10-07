from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from eligibility import check_basic_eligibility
from rag import search_documents


app = FastAPI(
    title="AI Legal Rights Navigator API",
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
        "project":
        "AI-Powered Legal Rights Navigator",

        "status":
        "Backend is running",

        "features": [
            "Eligibility Engine",
            "RAG Search",
            "Government Knowledge Base"
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
