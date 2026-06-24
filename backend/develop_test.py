from core.parser import extract_text
from core.chunker import split_requirements
from core.embedder import generate_embeddings
from rag_pipeline import store_requirements

# PDF path
pdf_path = "sample_docs/Online_Shopping_System_SRS.pdf"

# --------------------------------------------------
# STEP 1 : Extract text
# --------------------------------------------------

text = extract_text(pdf_path)

print("=" * 60)
print("STEP 1 : EXTRACTED TEXT")
print("=" * 60)

print(text[:1000])

print("\n")

# --------------------------------------------------
# STEP 2 : Split into requirements
# --------------------------------------------------

requirements = split_requirements(text)

print("=" * 60)
print("STEP 2 : REQUIREMENTS")
print("=" * 60)

print("Total Requirements:", len(requirements))

print()

for req in requirements[:5]:
    print(req)

print("\n")

# --------------------------------------------------
# STEP 3 : Generate embeddings
# --------------------------------------------------

embedded_requirements = generate_embeddings(requirements)

print("=" * 60)
print("STEP 3 : EMBEDDINGS")
print("=" * 60)

for item in embedded_requirements[:3]:

    print("Requirement ID :", item["id"])

    print("Requirement :", item["text"])

    print("Embedding Length :", len(item["embedding"]))

    print("First 10 Values :")

    print(item["embedding"][:10])

    print("-" * 60)

    # --------------------------------------------------
# STEP 4 : Store in ChromaDB
# --------------------------------------------------

print("\n")

print("=" * 60)
print("STEP 4 : STORE IN CHROMADB")
print("=" * 60)

store_requirements(embedded_requirements)