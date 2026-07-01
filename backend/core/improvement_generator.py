import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_improvement(
    requirement,
    completeness,
    ambiguity,
    knowledge
):

    prompt = f"""
You are an expert Software Requirements Engineer.

Your task is to rewrite poor software requirements into a high-quality IEEE 29148 compliant requirement.

Original Requirement:
{requirement}

Completeness Analysis:
{json.dumps(completeness, indent=4)}

Ambiguity Analysis:
{json.dumps(ambiguity, indent=4)}

Reference Knowledge:
{knowledge}

Instructions:

1. Read the original requirement.
2. Consider ALL missing information from the completeness analysis.
3. Consider ALL ambiguity issues.
4. Use the IEEE knowledge as guidance.
5. Rewrite the requirement into a SMART requirement.
6. Add measurable values whenever possible.
7. Use "shall" instead of weak words.
8. Return ONLY ONE valid JSON object.
9. Do NOT explain anything.
10. Do NOT use markdown.
11. Do NOT return multiple JSON objects.

Example:

{{
    "improved_requirement": "The system shall allow registered users to log in within 2 seconds under normal operating conditions.",
    "reason": "Added actor, measurable response time, condition and removed ambiguity."
}}
"""

    payload = {
        "model": "phi3:mini",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    response.raise_for_status()

    output = response.json()["response"]

    print("\n===================================")
    print("RAW IMPROVEMENT OUTPUT")
    print("===================================")
    print(output)

    # ---------------------------------
    # Remove Markdown if present
    # ---------------------------------

    output = output.replace("```json", "")
    output = output.replace("```", "")

    # ---------------------------------
    # Extract JSON only
    # ---------------------------------

    start = output.find("{")
    end = output.rfind("}") + 1

    if start == -1 or end == 0:

        print("\nNo JSON found in LLM output.")

        return {
            "improved_requirement": requirement,
            "reason": "LLM did not return valid JSON."
        }

    clean_json = output[start:end]

    print("\n===================================")
    print("EXTRACTED JSON")
    print("===================================")
    print(clean_json)

    # ---------------------------------
    # Parse JSON safely
    # ---------------------------------

    try:

        return json.loads(clean_json)

    except Exception as e:

        print("\nImprovement JSON Parsing Error")
        print(e)

        return {
            "improved_requirement": requirement,
            "reason": "Invalid JSON returned by LLM."
        }


    