import chromadb
from sentence_transformers import SentenceTransformer

extra_chunks = [
    "A requirement is a condition or capability that must be met or possessed by a system to satisfy a contract, standard, specification, or other formally imposed document.",
    "Ambiguity in requirements occurs when a statement can be interpreted in more than one way by different stakeholders, leading to inconsistent implementations.",
    "Lexical ambiguity arises when a word has multiple meanings. For example, the word 'fast' can mean quick execution or being fixed in place.",
    "Syntactic ambiguity occurs when the grammatical structure of a sentence allows multiple interpretations.",
    "A good requirement must be verifiable, meaning there must be a finite cost-effective process to check whether the software meets the requirement.",
    "Requirements completeness means that all conditions and capabilities needed by the user are documented with no gaps in functionality.",
    "A conflict in requirements exists when two or more requirements cannot both be satisfied simultaneously in the same system.",
    "Non-testable requirements use vague terms such as user-friendly, fast, reliable, or flexible without measurable criteria.",
]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(extra_chunks).tolist()

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("re_standards")

collection.add(
    documents=extra_chunks,
    embeddings=embeddings,
    metadatas=[{"source": "IREB Glossary", "chunk_id": i} for i in range(len(extra_chunks))],
    ids=[f"IREB-Glossary-{i}" for i in range(len(extra_chunks))]
)

print(f"Final count in re_standards: {collection.count()}")