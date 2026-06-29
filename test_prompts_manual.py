import pandas as pd
import json, re, requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

AMBIGUITY_PROMPT = """You are an IEEE 830 requirements engineer. Analyze this ONE requirement for ambiguity only.

Requirement: "{requirement}"

Respond with ONLY valid JSON, no extra text, no markdown:
{{"label": "ambiguous" or "ok", "confidence": 0.0, "ambiguous_terms": [], "reason": "one sentence", "suggested_revision": "text"}}"""

MISSING_PROMPT = """You are an IEEE 830 requirements engineer. Check if this requirement is missing an actor, measurable criteria, or condition.

Requirement: "{requirement}"

Respond with ONLY valid JSON, no extra text, no markdown:
{{"label": "missing" or "ok", "confidence": 0.0, "missing_elements": [], "reason": "one sentence", "suggested_revision": "text"}}"""

def call_llm(prompt):
    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.0}})
    return r.json()["response"]

def parse_json(raw):
    cleaned = re.sub(r"```json|```", "", raw).strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except:
        return None

df = pd.read_csv("ground_truth.csv", encoding="cp1252")
test_reqs = df["req_text"].head(20).tolist()

print("=== AMBIGUITY PROMPT TEST ===")
amb_success = 0
for i, req in enumerate(test_reqs):
    raw = call_llm(AMBIGUITY_PROMPT.format(requirement=req))
    result = parse_json(raw)
    ok = result is not None and "label" in result
    if ok: amb_success += 1
    print(f"[{i+1}] {'OK' if ok else 'FAIL'} | {req[:55]}...")
    if not ok: print(f"     RAW: {raw[:100]}")

print(f"\nAmbiguity success rate: {amb_success}/20 ({amb_success*5}%)")

print("\n=== MISSING PROMPT TEST ===")
mis_success = 0
for i, req in enumerate(test_reqs):
    raw = call_llm(MISSING_PROMPT.format(requirement=req))
    result = parse_json(raw)
    ok = result is not None and "label" in result
    if ok: mis_success += 1
    print(f"[{i+1}] {'OK' if ok else 'FAIL'} | {req[:55]}...")

print(f"\nMissing success rate: {mis_success}/20 ({mis_success*5}%)")