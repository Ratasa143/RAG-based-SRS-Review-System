def estimate_tokens(text: str) -> int:
    return len(text) // 4

def check_token_budget(prompt: str, limit: int = 2048) -> dict:
    count = estimate_tokens(prompt)
    return {
        "estimated_tokens": count,
        "within_budget": count <= limit,
        "warning": None if count <= limit else f"Prompt exceeds {limit} tokens ({count} estimated)"
    }