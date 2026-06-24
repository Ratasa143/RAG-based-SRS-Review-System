from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(requirements):
    """
    Generate embeddings for requirement objects.
    """

    embedded_requirements = []

    for req in requirements:

        embedding = model.encode(req["text"]).tolist()

        embedded_requirements.append({
            "id": req["id"],
            "text": req["text"],
            "embedding": embedding
        })

    return embedded_requirements