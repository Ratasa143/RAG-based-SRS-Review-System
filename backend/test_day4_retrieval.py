from rag_pipeline import retrieve_knowledge

# Test requirement
query = "The system should be fast."

print("=" * 60)
print("QUERY")
print("=" * 60)
print(query)

print()

# Search the knowledge base
results = retrieve_knowledge(query)

print("=" * 60)
print("RETRIEVED KNOWLEDGE")
print("=" * 60)

documents = results["documents"][0]
metadatas = results["metadatas"][0]

for i in range(len(documents)):

    print(f"Result {i+1}")

    print("Source :", metadatas[i]["source"])

    print()

    print(documents[i])

    print("-" * 60)