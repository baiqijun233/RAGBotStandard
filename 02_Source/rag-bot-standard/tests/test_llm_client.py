import unittest

from rag_bot.llm_client import (
    DEEPSEEK_CHAT_COMPLETIONS_URL,
    GROQ_CHAT_COMPLETIONS_URL,
    OPENAI_CHAT_COMPLETIONS_URL,
    get_default_base_url,
    get_default_model,
    parse_stream_content,
)


class LLMClientTests(unittest.TestCase):
    def test_groq_defaults_are_openai_compatible(self):
        self.assertEqual(get_default_model("Groq"), "llama-3.1-8b-instant")
        self.assertEqual(get_default_base_url("Groq"), GROQ_CHAT_COMPLETIONS_URL)

    def test_openai_defaults_are_openai_chat_completions(self):
        self.assertEqual(get_default_model("OpenAI"), "gpt-4o-mini")
        self.assertEqual(get_default_base_url("OpenAI"), OPENAI_CHAT_COMPLETIONS_URL)

    def test_deepseek_defaults_are_openai_compatible(self):
        self.assertEqual(get_default_model("DeepSeek"), "deepseek-v4-pro")
        self.assertEqual(get_default_base_url("DeepSeek"), DEEPSEEK_CHAT_COMPLETIONS_URL)

    def test_parse_stream_content_reads_openai_compatible_sse_lines(self):
        lines = [
            "data: {\"choices\":[{\"delta\":{\"content\":\"你\"}}]}\n".encode("utf-8"),
            b"\n",
            "data: {\"choices\":[{\"delta\":{\"content\":\"好\"}}]}\n".encode("utf-8"),
            b"data: [DONE]\n",
        ]

        self.assertEqual(list(parse_stream_content(lines)), ["你", "好"])

    def test_parse_stream_content_rejects_malformed_json(self):
        lines = [b"data: not-json\n"]

        with self.assertRaises(RuntimeError):
            list(parse_stream_content(lines))


if __name__ == "__main__":
    unittest.main()
