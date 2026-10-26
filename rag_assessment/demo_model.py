"""A deterministic model stand-in. It is intentionally simple, not an LLM."""

from typing import Any, Dict, List


def generate(question: str, passages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Return a short extractive answer from the top passage.

    The production boundary would call a real model here. This mock exists so
    the coding task is runnable offline and tests can inject bad model output.
    """
    if not passages:
        return {"answer": "", "citations": []}
    passage = passages[0]
    sentence = passage["text"].split(".", 1)[0].strip()
    return {"answer": sentence + ".", "citations": [passage["id"]]}
