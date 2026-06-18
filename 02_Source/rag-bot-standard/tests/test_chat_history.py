import unittest

from rag_bot.chat_history import add_message, clear_messages, get_messages


class ChatHistoryTests(unittest.TestCase):
    def test_add_message_keeps_role_and_content_order(self):
        state = {}

        add_message(state, "user", "你好")
        add_message(state, "assistant", "你好，我可以帮你读 PDF。")

        self.assertEqual(
            get_messages(state),
            [
                {"role": "user", "content": "你好"},
                {"role": "assistant", "content": "你好，我可以帮你读 PDF。"},
            ],
        )

    def test_add_message_rejects_blank_content(self):
        state = {}

        with self.assertRaises(ValueError):
            add_message(state, "user", "   ")

    def test_clear_messages_resets_history(self):
        state = {}
        add_message(state, "user", "问题")

        clear_messages(state)

        self.assertEqual(get_messages(state), [])


if __name__ == "__main__":
    unittest.main()
