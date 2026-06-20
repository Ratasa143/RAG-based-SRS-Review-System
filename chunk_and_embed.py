import fitz
import chromadb
from sentence_transformers import SentenceTransformer

def chunk_pdf(pdf_path, chunk_size=300, overlap=50):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    words = full_text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

docs = [
    ("incose_gtwr.pdf", "INCOSE GTWR v3"),
    ("ieee_830_1998.pdf", "IEEE 830-1998"),
]

all_chunks, all_metadata, all_ids = [], [], []

for filepath, source_name in docs:
    chunks = chunk_pdf(filepath)
    print(f"{source_name}: {len(chunks)} chunks")
    for i, chunk in enumerate(chunks):
        all_chunks.append(chunk)
        all_metadata.append({"source": source_name, "chunk_id": i})
        all_ids.append(f"{source_name.replace(' ','-')}-{i}")

print(f"\nTotal chunks: {len(all_chunks)}")

print("\nLoading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings...")
embeddings = model.encode(all_chunks, batch_size=32, show_progress_bar=True)

print("\nLoading into ChromaDB...")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("re_standards")

batch_size = 100
for i in range(0, len(all_chunks), batch_size):
    collection.add(
        documents=all_chunks[i:i+batch_size],
        embeddings=embeddings[i:i+batch_size].tolist(),
        metadatas=all_metadata[i:i+batch_size],
        ids=all_ids[i:i+batch_size]
    )
    print(f"Loaded batch {i//batch_size + 1}")

print(f"\nFinal count in re_standards: {collection.count()}")