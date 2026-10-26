import unittest

from rag_assessment.core import answer_question, insufficient_evidence, retrieve


DOCUMENTS = [
    {"id": "PUBLIC", "title": "Duplicate payment", "text": "Duplicate payment cases go to support review.", "access": ["general", "operations"]},
    {"id": "PRIVATE", "title": "Operations retry", "text": "Payment retry requires processor confirmation.", "access": ["operations"]},
    {"id": "OTHER", "title": "Refund", "text": "Refund requests go to the refunds queue.", "access": ["general", "operations"]},
]


class RetrievalTests(unittest.TestCase):
    def test_relevant_public_document(self):
        self.assertEqual(retrieve("duplicate payment", DOCUMENTS, "general", 1)[0]["id"], "PUBLIC")

    def test_role_is_enforced_before_model_sees_passages(self):
        seen = []

        def model(question, passages):
            seen.extend(passage["id"] for passage in passages)
            return {"answer": "Review the duplicate.", "citations": ["PUBLIC"]}

        answer_question("payment retry", "general", DOCUMENTS, model)
        self.assertNotIn("PRIVATE", seen)

    def test_unrelated_question_abstains_without_model_call(self):
        def model(question, passages):
            self.fail("model should not run without evidence")

        self.assertEqual(answer_question("weather forecast", "general", DOCUMENTS, model), insufficient_evidence())


class AnswerTests(unittest.TestCase):
    def test_valid_answer_has_citation_title(self):
        def model(question, passages):
            return {"answer": "Send it to support review.", "citations": ["PUBLIC"]}

        result = answer_question("duplicate payment", "general", DOCUMENTS, model)
        self.assertEqual(result, {"status": "answered", "answer": "Send it to support review.", "citations": [{"id": "PUBLIC", "title": "Duplicate payment"}]})

    def test_invented_citation_abstains(self):
        def model(question, passages):
            return {"answer": "An unsupported claim.", "citations": ["MADE-UP"]}

        self.assertEqual(answer_question("duplicate payment", "general", DOCUMENTS, model), insufficient_evidence())


if __name__ == "__main__":
    unittest.main()
