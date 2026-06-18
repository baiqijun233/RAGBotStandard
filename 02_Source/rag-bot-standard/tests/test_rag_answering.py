import unittest
from types import SimpleNamespace

from rag_bot.rag_answering import build_rag_prompt, answer_question


class FakeClient:
    def __init__(self):
        self.prompt = None

    def generate(self, prompt: str) -> str:
        self.prompt = prompt
        return "这是基于 PDF 内容生成的答案。"


class RagAnsweringTests(unittest.TestCase):
    def test_build_rag_prompt_includes_question_and_context(self):
        docs = [
            SimpleNamespace(page_content="第一段 PDF 内容", metadata={"source": "a.pdf"}),
            SimpleNamespace(page_content="第二段 PDF 内容", metadata={"source": "b.pdf"}),
        ]

        prompt = build_rag_prompt("这个文档讲什么？", docs)

        self.assertIn("这个文档讲什么？", prompt)
        self.assertIn("第一段 PDF 内容", prompt)
        self.assertIn("第二段 PDF 内容", prompt)
        self.assertIn("请用中文回答", prompt)

    def test_answer_question_uses_llm_client_when_available(self):
        docs = [SimpleNamespace(page_content="PDF 讲 RAG 系统。", metadata={})]
        client = FakeClient()

        result = answer_question("总结一下", docs, client)

        self.assertEqual(result.answer, "这是基于 PDF 内容生成的答案。")
        self.assertTrue(result.used_llm)
        self.assertEqual(len(result.sources), 1)
        self.assertIsNotNone(client.prompt)
        self.assertIn("总结一下", client.prompt)

    def test_answer_question_falls_back_without_llm_client(self):
        docs = [SimpleNamespace(page_content="PDF 讲向量检索。", metadata={})]

        result = answer_question("总结一下", docs, None)

        self.assertFalse(result.used_llm)
        self.assertIn("未配置 LLM", result.answer)
        self.assertEqual(result.sources[0].content, "PDF 讲向量检索。")


if __name__ == "__main__":
    unittest.main()
