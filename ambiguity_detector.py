import re
import pandas as pd

# Vague word lexicon
VAGUE_WORDS = [
    "fast", "quick", "quickly", "slow", "easy", "easily", "simple", "simply",
    "user-friendly", "friendly", "intuitive", "efficient", "efficiently",
    "adequate", "adequate", "sufficient", "sufficiently", "appropriate",
    "appropriately", "good", "better", "best", "high", "low", "large", "small",
    "many", "few", "several", "some", "various", "flexible", "scalable",
    "robust", "reliable", "reliably", "secure", "safely", "properly",
    "correctly", "accurately", "effectively", "effectively", "smoothly",
    "seamlessly", "optimally", "optimal", "maximum", "minimum", "minimal",
    "reasonable", "reasonably", "regularly", "periodically", "timely",
    "easily trainable", "user friendly", "high quality", "high performance",
    "as soon as possible", "in a timely manner", "as needed", "if necessary",
    "and so on", "etc", "and more", "and others", "or similar"
]

def rule_based_score(text):
    """
    Returns a score between 0 and 1 based on how many vague words are found.
    Also checks for regex patterns that indicate ambiguity.
    """
    text_lower = text.lower()
    
    # Count vague word matches
    matches = []
    for word in VAGUE_WORDS:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            matches.append(word)
    
    # Regex patterns that indicate ambiguity
    ambiguous_patterns = [
        r'\bshould\b',           # weak obligation
        r'\bmight\b',            # uncertainty
        r'\bcould\b',            # uncertainty  
        r'\bmay\b',              # uncertainty
        r'\bif (necessary|required|needed|applicable)\b',
        r'\band (so on|more|others)\b',
        r'\betc\.?\b',
        r'\bor similar\b',
        r'\bas (soon as possible|needed|required)\b',
        r'\bin a timely manner\b',
        r'\bappropriate(ly)?\b',
        r'\bsufficient(ly)?\b',
    ]
    
    pattern_matches = []
    for pattern in ambiguous_patterns:
        if re.search(pattern, text_lower):
            pattern_matches.append(pattern)
    
    total_matches = len(matches) + len(pattern_matches)
    
    # Score: 0 if no matches, scales up with more matches, max 1.0
    score = min(total_matches / 3.0, 1.0)
    
    return score, matches, pattern_matches

# Test it on a few examples
test_cases = [
    "The system shall respond quickly to user inputs",
    "The system shall authenticate users within 2 seconds using OAuth 2.0",
    "The UI should be user-friendly and easy to use",
    "The system shall encrypt all passwords using AES-256",
    "The software should work properly and efficiently",
]

print("Rule-based pre-filter test:\n")
for text in test_cases:
    score, vague, patterns = rule_based_score(text)
    print(f"Text: {text[:60]}...")
    print(f"Score: {score:.2f} | Vague words: {vague} | Patterns: {len(patterns)}")
    print()
    
import requests
import json

def llm_based_score(text):
    """
    Sends requirement to Mistral via Ollama and gets ambiguity confidence score.
    """
    prompt = f"""You are an expert requirements engineer.
Analyze this software requirement for ambiguity.
A requirement is ambiguous if it contains vague terms, has multiple interpretations, 
or lacks measurable criteria.

Requirement: "{text}"

Respond ONLY in valid JSON with no explanation:
{{"is_ambiguous": true/false, "confidence": 0.0-1.0, "reason": "one sentence"}}"""

    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        
        response_text = res.json()["response"].strip()
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            confidence = result.get("confidence", 0.0)
            if not result.get("is_ambiguous", False):
                confidence = 0.0
            return confidence, result.get("reason", "")
        return 0.0, "Could not parse response"
    
    except Exception as e:
        print(f"LLM error: {e}")
        return 0.0, "LLM unavailable"

# Test LLM on same examples
print("LLM-based analysis test:\n")
for text in test_cases[:3]:  # only first 3 to save time
    score, reason = llm_based_score(text)
    print(f"Text: {text[:60]}...")
    print(f"LLM Score: {score:.2f} | Reason: {reason}")
    print()
    
def combined_score(text, threshold=0.5):
    """
    Combines rule-based and LLM scores.
    Rule score acts as pre-filter — if 0, we still check LLM.
    Final: rule_score * 0.3 + llm_score * 0.7
    """
    rule_score, vague_words, patterns = rule_based_score(text)
    llm_score, reason = llm_based_score(text)
    
    final_score = (rule_score * 0.3) + (llm_score * 0.7)
    is_ambiguous = final_score >= threshold
    
    return {
        "text": text,
        "rule_score": round(rule_score, 2),
        "llm_score": round(llm_score, 2),
        "final_score": round(final_score, 2),
        "is_ambiguous": is_ambiguous,
        "vague_words": vague_words,
        "reason": reason
    }

# Test combined scoring
print("Combined scoring test:\n")
for text in test_cases:
    result = combined_score(text)
    print(f"Text: {text[:60]}...")
    print(f"Rule: {result['rule_score']} | LLM: {result['llm_score']} | Final: {result['final_score']} | Ambiguous: {result['is_ambiguous']}")
    print(f"Reason: {result['reason']}")
    print()