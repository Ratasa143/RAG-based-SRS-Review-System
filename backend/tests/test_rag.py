import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[2]))

import pandas as pd
from backend.core.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()

df = pd.read_csv("ground_truth.csv")

test_requirements = df["req_text"].head(20).tolist()

for i, req in enumerate(test_requirements, 1):
    print("=" * 80)
    print(f"Requirement {i}")
    print(req)
    print()

    result = pipeline.analyze_ambiguity(req)

    print("Result:")
    print(result)