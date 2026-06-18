from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from utils.pdf_handler import load_pdf_text


def get_vectorstore(uploaded_files):
    raw_text = load_pdf_text(uploaded_files)

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_texts(
        texts=[raw_text],
        embedding=embeddings
    )

    return vectorstore