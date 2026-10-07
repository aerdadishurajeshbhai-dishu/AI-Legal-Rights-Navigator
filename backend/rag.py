import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "backend/chroma_db"

client = chromadb.PersistentClient(
    path=DB_PATH
)

collection = client.get_or_create_collection(
    name="government_knowledge"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def search_documents(query, top_k=5):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    output = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        output.append({
            "text": document,
            "metadata": metadata
        })

    return output
