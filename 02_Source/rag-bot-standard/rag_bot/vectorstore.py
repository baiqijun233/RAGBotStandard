import hashlib
from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from rag_bot.pdf_loader import extract_pdf_text, split_text


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_COLLECTION_NAME = "rag_pdf_default"


def get_default_chroma_directory(source_file: Path | None = None) -> Path:
    current_file = Path(source_file or __file__).resolve(strict=False)
    project_root = current_file.parents[3]
    return project_root / "04_Data" / "chroma"


def make_collection_name(file_names: tuple[str, ...], file_bytes: tuple[bytes, ...]) -> str:
    digest = hashlib.sha256()
    for name, data in zip(file_names, file_bytes, strict=True):
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(data)
        digest.update(b"\0")
    return f"rag_pdf_{digest.hexdigest()[:16]}"


def make_chunk_ids(collection_name: str, chunks: list[str]) -> list[str]:
    ids: list[str] = []
    for index, chunk in enumerate(chunks):
        digest = hashlib.sha256()
        digest.update(collection_name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(index).encode("utf-8"))
        digest.update(b"\0")
        digest.update(chunk.encode("utf-8"))
        ids.append(f"{collection_name}_{digest.hexdigest()[:16]}")
    return ids


def build_vectorstore(
    uploaded_files,
    persist_directory: str | Path | None = None,
    collection_name: str = DEFAULT_COLLECTION_NAME,
):
    files = list(uploaded_files)
    raw_text = extract_pdf_text(files)
    chunks = split_text(raw_text)

    if not chunks:
        raise ValueError("No readable text was found in the uploaded PDF files.")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    chroma_directory = Path(persist_directory) if persist_directory else get_default_chroma_directory()
    chroma_directory.mkdir(parents=True, exist_ok=True)

    return Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        ids=make_chunk_ids(collection_name, chunks),
        persist_directory=str(chroma_directory),
        collection_name=collection_name,
    )
