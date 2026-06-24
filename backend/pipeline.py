from core.parser import extract_text
from core.chunker import split_requirements
from rag_pipeline import retrieve_knowledge
from core.llm import analyze_requirement


def analyze_document(pdf_path):
    """
    Complete AI Pipeline

    PDF
      ↓
    Parser
      ↓
    Chunker
      ↓
    Retriever
      ↓
    LLM
      ↓
    Final JSON
    """

    # ----------------------------------------
    # STEP 1 : Extract text from PDF
    # ----------------------------------------

    print("\nSTEP 1 : Extracting text from PDF...")

    text = extract_text(pdf_path)

    print("Text extracted successfully.")

    # ----------------------------------------
    # STEP 2 : Split into requirements
    # ----------------------------------------

    print("\nSTEP 2 : Splitting into requirements...")

    requirements = split_requirements(text)

    print(f"Total requirements found: {len(requirements)}")

    # ----------------------------------------
    # IMPORTANT
    # During testing we analyze ONLY first 3.
    # Later change back to all requirements.
    # ----------------------------------------

    requirements = requirements[:3]

    print(f"Testing only first {len(requirements)} requirements.\n")

    final_results = []

    # ----------------------------------------
    # STEP 3 : Analyze each requirement
    # ----------------------------------------

    for req in requirements:

        print("=" * 60)
        print(f"Analyzing {req['id']}")
        print("=" * 60)

        print("Requirement:")
        print(req["text"])
        print()

        # ----------------------------------------
        # Retrieve knowledge
        # ----------------------------------------

        print("Searching Knowledge Base...")

        retrieved = retrieve_knowledge(req["text"])

        knowledge = ""

        for document in retrieved["documents"][0]:
            knowledge += document + "\n"

        print("Knowledge Retrieved.\n")

        # ----------------------------------------
        # Send to LLM
        # ----------------------------------------

        print("Sending to LLM...")

        analysis = analyze_requirement(
            req["text"],
            knowledge
        )

        print("LLM Response Received.\n")

        final_results.append({
            "id": req["id"],
            "text": req["text"],
            "analysis": analysis
        })

        print(f"{req['id']} Completed.\n")

    print("=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    return final_results