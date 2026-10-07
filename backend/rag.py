import os
import chromadb

from sentence_transformers import SentenceTransformer


DB_PATH = "./chroma_db"

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(
    name="government_knowledge"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def add_document(
    document_id,
    text,
    source_url,
    metadata=None
):

    embedding = embedding_model.encode(
        text
    ).tolist()

    metadata = metadata or {}

    metadata["source_url"] = source_url

    collection.add(
        ids=[document_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )


def search_documents(query, top_k=5):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    output = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        output.append({
            "text": document,
            "source": metadata.get(
                "source_url"
            ),
            "metadata": metadata
        })

    return output
