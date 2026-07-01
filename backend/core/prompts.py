AMBIGUITY_PROMPT = """You are an IEEE 830 requirements engineer. Analyze ONE requirement for ambiguity only.

Relevant standard excerpts:
{context}

Requirement: "{requirement}"

Respond with ONLY valid JSON, no other text:
{{"label": "ambiguous" or "ok", "confidence": 0.0-1.0, "ambiguous_terms": ["term1"], "reason": "one sentence", "suggested_revision": "improved text"}}"""

CONFLICT_PROMPT = """You are an IEEE 830 requirements engineer. Determine if these two requirements conflict.

Relevant standard excerpts:
{context}

Requirement A: "{requirement_a}"
Requirement B: "{requirement_b}"

Respond with ONLY valid JSON, no other text:
{{"label": "conflict" or "ok", "confidence": 0.0-1.0, "conflict_type": "direct_contradiction" or "scope_overlap" or "none", "reason": "one sentence"}}"""

MISSING_PROMPT = """You are an IEEE 830 requirements engineer. Check if this requirement is missing key information (actor, measurable criteria, condition).

Relevant standard excerpts:
{context}

Requirement: "{requirement}"

Respond with ONLY valid JSON, no other text:
{{"label": "missing" or "ok", "confidence": 0.0-1.0, "missing_elements": ["actor"], "reason": "one sentence", "suggested_revision": "improved text"}}"""

SUGGEST_PROMPT = """You are an IEEE 830 requirements engineer. Rewrite this requirement to be specific, measurable, and testable (SMART).

Relevant standard excerpts:
{context}

Original requirement: "{requirement}"

Respond with ONLY valid JSON, no other text:
{{"original": "{requirement}", "improved": "rewritten requirement", "changes_made": "one sentence explaining what changed"}}"""