import unittest

from rag_bot.pdf_loader import split_text


class PdfLoaderTests(unittest.TestCase):
    def test_split_text_returns_empty_list_for_blank_text(self):
        self.assertEqual(split_text("   "), [])


    def test_split_text_splits_long_text(self):
        text = "alpha beta gamma " * 200

        chunks = split_text(text, chunk_size=80, chunk_overlap=10)

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(chunk.strip() for chunk in chunks))


if __name__ == "__main__":
    unittest.main()
