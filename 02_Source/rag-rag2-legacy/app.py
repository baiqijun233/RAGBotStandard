import streamlit as st
from utils.vectorstore_handler import get_vectorstore

st.title("RAG Bot 2.0 (Stable Version)")

uploaded_files = st.file_uploader("Upload PDFs", accept_multiple_files=True)
query = st.text_input("Ask a question")

vectorstore = None
retriever = None

# ⚠️ 必须先判断文件
if uploaded_files:
    vectorstore = get_vectorstore(uploaded_files)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ⚠️ 再判断 query
if query and retriever:
    docs = retriever.invoke(query)   # 新版 LangChain 必须用 invoke
    st.write(docs[0].page_content if docs else "No result")