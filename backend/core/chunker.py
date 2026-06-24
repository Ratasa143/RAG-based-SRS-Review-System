import re

# Requirement keywords commonly used in SRS documents
KEYWORDS = [
    "shall",
    "should",
    "must",
    "may",
    "will"
]


def split_requirements(text):
    """
    Split extracted PDF text into individual requirement objects.
    """

    # Split the document into individual lines
    lines = text.split("\n")

    requirements = []
    count = 1

    for line in lines:

        # Remove extra spaces
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip very short lines
        if len(line) < 15:
            continue

        # Skip very long paragraphs
        if len(line) > 300:
            continue

        # Convert to lowercase for comparison
        lower = line.lower()

        # -----------------------------------------
        # Ignore common headings
        # -----------------------------------------

        if lower.startswith("page"):
            continue

        if lower.startswith("table of"):
            continue

        if lower.startswith("chapter"):
            continue

        if lower.startswith("figure"):
            continue

        if lower.startswith("contents"):
            continue

        if lower.startswith("appendix"):
            continue

        # -----------------------------------------
        # Ignore document information
        # -----------------------------------------

        IGNORE_WORDS = [
            "submitted by",
            "submitted to",
            "department",
            "university",
            "members",
            "abstract",
            "introduction",
            "objective",
            "scope",
            "definition",
            "overview",
            "references",
            "bibliography",
            "acknowledgement",
            "table of contents"
        ]

        if any(word in lower for word in IGNORE_WORDS):
            continue

        # -----------------------------------------
        # Ignore numbering only
        # Examples:
        # 1
        # 2.1
        # 5.4.2
        # -----------------------------------------

        if re.fullmatch(r"[0-9. ]+", line):
            continue

        # -----------------------------------------
        # Ignore names beginning with ->
        # Example:
        # ->Amlan Tribedi
        # -----------------------------------------

        if line.startswith("->"):
            continue

        # -----------------------------------------
        # Accept only requirement-like sentences
        # -----------------------------------------

        if any(keyword in lower for keyword in KEYWORDS):

            requirements.append({
                "id": f"R{count}",
                "text": line
            })

            count += 1

    return requirements