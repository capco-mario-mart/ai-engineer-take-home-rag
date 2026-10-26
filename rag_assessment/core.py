"""Implement the retrieval and answer-validation boundary here."""

from typing import Any, Callable, Dict, List


INSUFFICIENT_ANSWER = "I don't have enough reliable information to answer that."


def insufficient_evidence() -> Dict[str, Any]:
    return {"status": "insufficient_evidence", "answer": INSUFFICIENT_ANSWER, "citations": []}


def retrieve(question: str, documents: List[Dict[str, Any]], role: str, limit: int = 3) -> List[Dict[str, Any]]:
    """Return relevant documents visible to role, most relevant first.

    Each document has id, title, text, and access (a list of allowed roles).
    Empty or unrelated questions should return []. Do not mutate documents.
    """
    # TODO: Implement role filtering, deterministic relevance ranking, and limit.
    raise NotImplementedError


def answer_question(
    question: str,
    role: str,
    documents: List[Dict[str, Any]],
    model: Callable[[str, List[Dict[str, Any]]], Dict[str, Any]],
) -> Dict[str, Any]:
    """Retrieve evidence, invoke the model, and validate its answer and citations.

    The model takes (question, retrieved_documents) and returns a dict with
    answer (str) and citations (list of document ID strings). Its output is
    untrusted and may be malformed.
    """
    # TODO: Call retrieve and then model only when evidence exists. Validate
    # the model's answer/citations and return the documented response shape.
    raise NotImplementedError
