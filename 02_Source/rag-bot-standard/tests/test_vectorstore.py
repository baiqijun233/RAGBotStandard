import unittest
from pathlib import Path

from rag_bot.vectorstore import get_default_chroma_directory, make_chunk_ids, make_collection_name


class VectorstoreTests(unittest.TestCase):
    def test_default_chroma_directory_stays_inside_project_data_folder(self):
        source_file = (
            Path("E:/Agent/AIProjects/Project001_RAGBotStandard")
            / "02_Source"
            / "rag-bot-standard"
            / "rag_bot"
            / "vectorstore.py"
        )

        self.assertEqual(
            get_default_chroma_directory(source_file),
            Path("E:/Agent/AIProjects/Project001_RAGBotStandard/04_Data/chroma"),
        )

    def test_make_collection_name_is_stable_and_changes_with_file_content(self):
        first = make_collection_name(("a.pdf",), (b"same bytes",))
        second = make_collection_name(("a.pdf",), (b"same bytes",))
        changed = make_collection_name(("a.pdf",), (b"different bytes",))

        self.assertEqual(first, second)
        self.assertNotEqual(first, changed)
        self.assertTrue(first.startswith("rag_pdf_"))

    def test_make_chunk_ids_are_stable_for_same_collection_and_chunks(self):
        first = make_chunk_ids("rag_pdf_abc", ["chunk one", "chunk two"])
        second = make_chunk_ids("rag_pdf_abc", ["chunk one", "chunk two"])
        changed = make_chunk_ids("rag_pdf_abc", ["chunk one changed", "chunk two"])

        self.assertEqual(first, second)
        self.assertNotEqual(first, changed)
        self.assertEqual(len(first), 2)


if __name__ == "__main__":
    unittest.main()
