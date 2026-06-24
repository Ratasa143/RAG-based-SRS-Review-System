import os
import chromadb

from core.embedder import model

# --------------------------------------------------
# Create Persistent ChromaDB Client
# --------------------------------------------------

client = chromadb.PersistentClient(path="db")

# --------------------------------------------------
# Collection for SRS Requirements
# --------------------------------------------------

requirements_collection = client.get_or_create_collection(
    name="requirements"
)

# --------------------------------------------------
# Collection for Knowledge Base
# --------------------------------------------------

knowledge_collection = client.get_or_create_collection(
    name="knowledge_base"
)

# --------------------------------------------------
# Store SRS Requirements
# --------------------------------------------------

def store_requirements(embedded_requirements):
    """
    Store SRS requirement embeddings in ChromaDB.
    """

    for req in embedded_requirements:

        requirements_collection.add(
            ids=[req["id"]],
            documents=[req["text"]],
            embeddings=[req["embedding"]]
        )

    print(f"\nStored {len(embedded_requirements)} requirements in ChromaDB.")

# --------------------------------------------------
# Load Knowledge Base Documents
# --------------------------------------------------

def load_knowledge_base(folder_path):
    """
    Read all .txt files from knowledge_base/documents,
    generate embeddings, and store them in ChromaDB.
    """

    count = 1

    for filename in os.listdir(folder_path):

        if filename.endswith(".txt"):

            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            embedding = model.encode(text).tolist()

            knowledge_collection.add(
                ids=[f"K{count}"],
                documents=[text],
                embeddings=[embedding],
                metadatas=[{"source": filename}]
            )

            print(f"Loaded: {filename}")

            count += 1

    print("\nKnowledge Base Loaded Successfully.")
    # --------------------------------------------------
# Retrieve Knowledge
# --------------------------------------------------

def retrieve_knowledge(query, n_results=3):
    """
    Search the knowledge base for the most relevant documents.
    """

    # Convert query into embedding
    query_embedding = model.encode(query).tolist()

    # Search ChromaDB
    results = knowledge_collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results
    