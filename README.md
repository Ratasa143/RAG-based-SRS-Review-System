# RAG-Based SRS Review System

## Week 1 - Briana's Setup (re_standards Knowledge Base)

### What I did
- Installed Ollama + Mistral 7B (local LLM)
- Set up ChromaDB with 4 collections
- Chunked IEEE 830 + INCOSE documents and embedded them
- re_standards collection now has 201 chunks ready for retrieval

### ⚠️ Important for teammates
The `chroma_db/` folder is already populated with 201 embeddings.
DO NOT run `chunk_and_embed.py` or `topup.py` again — it will cause duplicate entries.

### Setup instructions (run these once on your machine)

**1. Install dependencies**
pip install chromadb sentence-transformers pymupdf requests

**2. Install Ollama**
Download from https://ollama.ai and run:
ollama pull mistral

**3. Verify the knowledge base is working**
python test_chromadb.py

### Files in this project
- `test_ollama.py` — tests Ollama + Mistral is working
- `setup_chromadb.py` — creates the 4 ChromaDB collections (already done)
- `chunk_and_embed.py` — chunks PDFs and loads into ChromaDB (already done)
- `topup.py` — adds extra IREB glossary chunks (already done)
- `chroma_db/` — vector database, already populated, do not delete

### Collections in ChromaDB
- `re_standards` — 201 chunks (IEEE 830 + INCOSE + IREB) ✅
- `re_patterns` — empty, to be filled next week
- `ambiguity_lexicon` — empty, to be filled next week
- `conflict_patterns` — empty, to be filled next week