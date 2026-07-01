import json
import re
import requests
import chromadb
from sentence_transformers import SentenceTransformer
from core.prompts import AMBIGUITY_PROMPT, CONFLICT_PROMPT, MISSING_PROMPT, SUGGEST_PROMPT

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

class RAGPipeline:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="../chroma_db")
        self.collection = self.client.get_collection("re_standards")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def retrieve_context(self, query: str, top_k: int = 3) -> str:
        query_embedding = self.embedder.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        chunks = results["documents"][0]
        return "\n---\n".join(chunks)

    def call_llm(self, prompt: str) -> str:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1}
        })
        return response.json()["response"]

    def parse_json_output(self, raw_output: str) -> dict:
        cleaned = re.sub(r"```json|```", "", raw_output).strip()
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            return {"error": "no_json_found", "raw": raw_output}
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return {"error": "invalid_json", "raw": raw_output}

    def analyze_ambiguity(self, requirement: str) -> dict:
        context = self.retrieve_context(requirement)
        prompt = AMBIGUITY_PROMPT.format(context=context, requirement=requirement)
        raw = self.call_llm(prompt)
        return self.parse_json_output(raw)

    def analyze_missing(self, requirement: str) -> dict:
        context = self.retrieve_context(requirement)
        prompt = MISSING_PROMPT.format(context=context, requirement=requirement)
        raw = self.call_llm(prompt)
        return self.parse_json_output(raw)

    def analyze_conflict(self, requirement_a: str, requirement_b: str) -> dict:
        context = self.retrieve_context(requirement_a)
        prompt = CONFLICT_PROMPT.format(context=context, requirement_a=requirement_a, requirement_b=requirement_b)
        raw = self.call_llm(prompt)
        return self.parse_json_output(raw)

    def suggest_improvement(self, requirement: str) -> dict:
        context = self.retrieve_context(requirement)
        prompt = SUGGEST_PROMPT.format(context=context, requirement=requirement)
        raw = self.call_llm(prompt)
        return self.parse_json_output(raw)
    

from core.token_utils import check_token_budget

# inside analyze_ambiguity (and the other 3 methods), after prompt = ...format(...):
budget_check = check_token_budget(prompt)
if not budget_check["within_budget"]:
    print(f"WARNING: {budget_check['warning']}")