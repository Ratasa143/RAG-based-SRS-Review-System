from core.llm import analyze_requirement

requirement = "The system should be fast."

knowledge = """
Requirements should be measurable.

Avoid vague words.

Use SHALL instead of SHOULD.
"""

print("=" * 60)
print("LLM ANALYSIS")
print("=" * 60)

response = analyze_requirement(
    requirement,
    knowledge
)

print(response)