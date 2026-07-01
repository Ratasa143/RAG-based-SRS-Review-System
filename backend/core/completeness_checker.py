import json
import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def check_completeness(requirement):

    prompt = f"""
You are an expert Software Requirements Engineer.

Analyze the following software requirement.

Requirement:
{requirement}

Determine whether the requirement contains:

1. Actor
2. Action
3. Condition
4. Quality Criteria

Rules:

- Return ONLY ONE valid JSON object.
- Do NOT explain anything.
- Do NOT use markdown.
- Do NOT write ```json.
- Do NOT add comments.
- Do NOT write text before or after the JSON.
- The first character must be {{
- The last character must be }}

Example:

{{
    "actor": true,
    "action": true,
    "condition": false,
    "quality_criteria": false,
    "missing": [
        "Condition",
        "Quality Criteria"
    ],
    "score": 0.50
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

    print("\n" + "=" * 60)
    print("RAW COMPLETENESS OUTPUT")
    print("=" * 60)
    print(output)
    print("=" * 60)

    # -------------------------------------------------
    # Remove markdown
    # -------------------------------------------------

    output = output.replace("```json", "")
    output = output.replace("```", "")

    # -------------------------------------------------
    # Remove JavaScript style comments
    # -------------------------------------------------

    output = re.sub(r"//.*", "", output)

    # -------------------------------------------------
    # Extract JSON object
    # -------------------------------------------------

    start = output.find("{")
    end = output.rfind("}") + 1

    if start == -1 or end == 0:

        print("No JSON object found.")

        return {
            "actor": False,
            "action": False,
            "condition": False,
            "quality_criteria": False,
            "missing": [
                "Unable to parse LLM response"
            ],
            "score": 0
        }

    clean_json = output[start:end]

    print("\nExtracted JSON:\n")
    print(clean_json)

    try:

        parsed = json.loads(clean_json)

        print("\nSuccessfully Parsed JSON\n")

        return parsed

    except json.JSONDecodeError as e:

        print("\nJSON Parsing Error")
        print(e)

        return {
            "actor": False,
            "action": False,
            "condition": False,
            "quality_criteria": False,
            "missing": [
                "Invalid JSON returned by LLM"
            ],
            "score": 0
        }