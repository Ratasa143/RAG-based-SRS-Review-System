# RAG-Based SRS Review System

## Week 1 - namrata's Setup (re_standards Knowledge Base)

### What I did
- Installed Ollama + Mistral 7B (local LLM)
- Set up ChromaDB with 4 collections
- Chunked IEEE 830 + INCOSE documents and embedded them
- re_standards collection now has 201 chunks ready for retrieval

### Week 2 - namrata's Setup (Dataset Labeling & Evaluation Pipeline)

### What I did
- Downloaded PURE dataset from Zenodo (https://zenodo.org/records/1414117)
- Extracted requirements from 3 SRS documents (keepass, microcare, dii)
- Manually labeled 100 requirements as ok/ambiguous/missing/conflict
- Built evaluation pipeline with precision, recall, F1, accuracy
- Created Jupyter notebook with confusion matrix visualization

### ⚠️ Important for teammates
- The `chroma_db/` folder is already populated with 201 embeddings.
  DO NOT run `chunk_and_embed.py` or `topup.py` again — it will cause duplicate entries.
- `ground_truth.csv` has 100 labeled requirements — do not relabel them.
- To add more labels, open `ground_truth.csv` in Excel and fill in the
  `true_label` column for rows that are empty.

### Setup instructions (run these once on your machine)

**1. Install dependencies**
pip install chromadb sentence-transformers pymupdf requests pandas scikit-learn matplotlib seaborn jupyter

**2. Install Ollama**
Download from https://ollama.ai and run:
ollama pull mistral

**3. Verify the knowledge base is working**
python test_chromadb.py

**4. Run the evaluation pipeline**
python evaluation.py

**5. Open the Jupyter notebook**
python -m notebook
Then open evaluation.ipynb

### Files in this project
- `test_ollama.py` — tests Ollama + Mistral is working
- `setup_chromadb.py` — creates the 4 ChromaDB collections (already done)
- `chunk_and_embed.py` — chunks PDFs and loads into ChromaDB (already done)
- `topup.py` — adds extra IREB glossary chunks (already done)
- `parse_xml.py` — extracts requirements from PURE SRS XML files
- `evaluation.py` — computes precision, recall, F1, accuracy
- `evaluation.ipynb` — Jupyter notebook with confusion matrix
- `ground_truth.csv` — 100 manually labeled requirements
- `chroma_db/` — vector database, already populated, do not delete

### Collections in ChromaDB
- `re_standards` — 201 chunks (IEEE 830 + INCOSE + IREB) ✅
- `re_patterns` — empty, to be filled next week
- `ambiguity_lexicon` — empty, to be filled next week
- `conflict_patterns` — empty, to be filled next week

### Label Distribution (ground_truth.csv)
- ok: 52
- missing: 35
- ambiguous: 13
- conflict: 0 (rare in this document)
