import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def analyze_requirement(requirement, knowledge):

    prompt = f"""
You are an expert Software Requirements Engineer.

Knowledge Base:
{knowledge}

Requirement:
{requirement}

Analyze ONLY this requirement.

Return ONLY ONE valid JSON object.

Do NOT use Markdown.

Do NOT use triple backticks.

Do NOT explain anything.

Return exactly in this format:

{{
    "issue": "",
    "suggestion": "",
    "confidence": ""
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

    return response.json()["response"]