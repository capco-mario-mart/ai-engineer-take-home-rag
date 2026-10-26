# AI Engineer take-home: grounded answers

**Time box:** 45–60 minutes. Please stop after one hour and note any unfinished work in your PR.

## Scenario

You are adding a question-answering endpoint for a fictional payment operations team. The service retrieves short knowledge-base passages, sends the permitted passages to a model, and returns an answer with source citations. The supplied model is deterministic so the exercise needs no account, API key, database, or network access. All data is synthetic.

The HTTP endpoint and mock model are already wired up. Complete the two functions marked `TODO` in `rag_assessment/core.py`:

1. `retrieve`: Find up to `limit` relevant passages for the question. Only pass passages to the model when the requested role is allowed to see them. Rank by a simple, explainable relevance rule; a vector database is **not** required. Return no passages for an unrelated question. Make ties deterministic.
2. `answer_question`: Call `retrieve`, then call the supplied model only if evidence was found. Return an answer only when the model returns a nonempty answer and every citation is a distinct ID from the retrieved passages. Otherwise return the provided `insufficient_evidence()` response. Do not return restricted passages or unsupported citation IDs. Treat malformed model output as insufficient evidence.

You may add small helpers or tests. Keep the public function signatures and response shape so the endpoint keeps working. Use the existing Python standard library only.

## Run it

Requires Python 3.9 or newer.
The supplied tests fail on the starter branch because the two functions still raise `NotImplementedError`.

```bash
python3 -m unittest discover -s tests -v
python3 -m rag_assessment.api
```

In another terminal:

```bash
curl -s http://localhost:8000/answer \
  -H 'Content-Type: application/json' \
  -d '{"question":"When should a duplicate payment be escalated?","role":"general"}'
```

`role` is either `general` or `operations`. A general user may see passages with `access: ["general", "operations"]`; an operations user may also see passages with `access: ["operations"]`.

## What to submit

Fork this public repository, clone your fork, create a branch, and open a PR from your fork against this repository's `main` branch. Include your code, at least two meaningful tests beyond the supplied tests, and a brief PR description covering:

- Your relevance rule and its limitations.
- What you would change for a production RAG service with an actual LLM and enterprise documents.
- Any AI coding assistance you used and how you checked its output.

We assess correctness, privacy and grounding behavior, tests, and engineering judgment. We do **not** expect a production deployment, vector database, polished UI, or work beyond the time box. The reviewer may ask you to explain a design choice in the interview.

## API shape

`POST /answer` takes `{"question": "...", "role": "general"}` and returns:

```json
{
  "status": "answered",
  "answer": "...",
  "citations": [{"id": "KB-001", "title": "..."}]
}
```

When evidence is missing or invalid, return `{"status": "insufficient_evidence", "answer": "I don't have enough reliable information to answer that.", "citations": []}`.

The task tests the retrieval and validation boundary. Citation validation by itself cannot prove that natural-language claims are true; we will discuss that distinction in the review.
