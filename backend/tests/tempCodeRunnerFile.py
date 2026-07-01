import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.core.rag_pipeline import RAGPipeline

import pandas as pd

pipeline = RAGPipeline()

df = pd.read_csv("ground_truth.csv")

test_requirements = df["req_text"].head(20).tolist()

for i, req in enumerate(test_requirements, 1):
    print(f"\nRequirement {i}:")
    print(req)

    result = pipeline.analyze_ambiguity(req)
    print(result)
