import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("re_standards")
print(f"re_standards count: {collection.count()}")

model = SentenceTransformer("all-MiniLM-L6-v2")
query = "What makes a requirement ambiguous?"
embedding = model.encode([query])[0].tolist()

results = collection.query(query_embeddings=[embedding], n_results=2)
print("\nSample retrieval result:")
print(results["documents"][0][0][:300])