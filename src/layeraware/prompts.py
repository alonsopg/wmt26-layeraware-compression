import json
from pathlib import Path

PROMPTS = {
    "ces-deu": "Translate the following text from Czech to German. Output only the translation.\n\n{source}",
    "eng-zho_Hans": "Translate the following text from English to Simplified Chinese. Output only the translation.\n\n{source}",
    "eng-ara_EG": "Translate the following text from English to Egyptian Arabic. Output only the translation.\n\n{source}",
}

def render(lang_pair: str, source: str) -> str:
    return PROMPTS[lang_pair].format(source=source)

def save(path: str | Path) -> None:
    Path(path).write_text(json.dumps(PROMPTS, indent=2, ensure_ascii=False) + "\n")
