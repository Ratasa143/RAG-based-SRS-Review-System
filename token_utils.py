def estimate_tokens(text: str) -> int:
    return len(text) // 4

def check_token_budget(prompt: str, limit: int = 2048) -> dict:
    count = estimate_tokens(prompt)
    return {
        "estimated_tokens": count,
        "within_budget": count <= limit,
        "warning": None if count <= limit else f"WARNING: prompt is ~{count} tokens (limit {limit})"
    }

if __name__ == "__main__":
    # Quick self-test
    test = "The system shall authenticate users within 2 seconds using OAuth 2.0." * 50
    result = check_token_budget(test)
    print(result)