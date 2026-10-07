import os
import hashlib
import fitz
import chromadb

from sentence_transformers import SentenceTransformer


DOCUMENTS_DIR = "data/documents"
DB_PATH = "backend/chroma_db"


# Chroma database
client = chromadb.PersistentClient(
    path=DB_PATH
)

collection = client.get_or_create_collection(
    name="government_knowledge"
)


# Embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_chunks(text, chunk_size=1000, overlap=150):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def get_file_hash(file_path):

    with open(file_path, "rb") as file:

        return hashlib.sha256(
            file.read()
        ).hexdigest()


def process_pdf(pdf_path):

    pdf = fitz.open(pdf_path)

    document_name = os.path.basename(
        pdf_path
    )

    document_hash = get_file_hash(
        pdf_path
    )

    print(
        f"\nProcessing: {document_name}"
    )

    for page_number, page in enumerate(pdf):

        text = page.get_text().strip()

        if not text:
            continue

        chunks = create_chunks(text)

        for chunk_number, chunk in enumerate(chunks):

            document_id = (
                f"{document_name}_"
                f"{page_number + 1}_"
                f"{chunk_number}"
            )

            embedding = embedding_model.encode(
                chunk
            ).tolist()

            collection.upsert(
                ids=[document_id],

                documents=[chunk],

                embeddings=[embedding],

                metadatas=[{
                    "document": document_name,
                    "page": page_number + 1,
                    "source_type":
                        "official_government_document",
                    "file_hash":
                        document_hash
                }]
            )

    pdf.close()

    print(
        f"Completed: {document_name}"
    )


def main():

    if not os.path.exists(
        DOCUMENTS_DIR
    ):

        print(
            "ERROR: data/documents folder "
            "does not exist."
        )

        return

    pdf_files = [
        file
        for file in os.listdir(
            DOCUMENTS_DIR
        )
        if file.lower().endswith(".pdf")
    ]

    if not pdf_files:

        print(
            "No PDF files found in "
            "data/documents/"
        )

        return

    for file in pdf_files:

        pdf_path = os.path.join(
            DOCUMENTS_DIR,
            file
        )

        process_pdf(pdf_path)

    print(
        "\nRAG ingestion completed successfully."
    )


if __name__ == "__main__":

    main()
