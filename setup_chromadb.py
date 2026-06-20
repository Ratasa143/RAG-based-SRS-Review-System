import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collections = ["re_standards", "re_patterns", "ambiguity_lexicon", "conflict_patterns"]

for name in collections:
    col = client.get_or_create_collection(name=name)
    print(f"Created: {name} — count: {col.count()}")