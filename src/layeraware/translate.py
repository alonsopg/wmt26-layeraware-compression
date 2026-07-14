def clean(text: str, fallback: str) -> str:
    value = " ".join(text.strip().splitlines()).strip()
    return value or fallback
