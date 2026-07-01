from core.improvement_generator import generate_improvement

requirement = "The system should be fast."

completeness = {
    "actor": True,
    "action": True,
    "condition": False,
    "quality_criteria": False,
    "missing": [
        "Condition",
        "Quality Criteria"
    ],
    "score": 0.5
}

ambiguity = {
    "issue": "Ambiguity",
    "suggestion": "Specify measurable values.",
    "confidence": "High"
}

knowledge = """
Requirements should avoid vague words.
Requirements should be measurable.
Use SHALL.
"""

result = generate_improvement(
    requirement,
    completeness,
    ambiguity,
    knowledge
)

print(result)