from io import BytesIO

import streamlit as st

from rag_bot.auth import authenticate, get_login_config
from rag_bot.chat_history import add_message, clear_messages, get_messages
from rag_bot.llm_client import (
    OpenAICompatibleClient,
    get_default_base_url,
    get_default_model,
    get_env_api_key,
)
from rag_bot.rag_answering import answer_question, build_rag_prompt, build_sources
from rag_bot.vectorstore import build_vectorstore, get_default_chroma_directory, make_collection_name


st.set_page_config(page_title="RAG Bot 2.0")


class UploadedPDF(BytesIO):
    def __init__(self, name: str, data: bytes):
        super().__init__(data)
        self.name = name


def require_login() -> bool:
    config = get_login_config()
    if st.session_state.get("authenticated"):
        return True

    st.title("RAG Bot 2.0 登录")
    if config.uses_default_password:
        st.info("本地默认账号：admin，默认密码：ragbot。正式使用前请设置 RAG_BOT_USERNAME 和 RAG_BOT_PASSWORD。")

    with st.form("login_form"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        submitted = st.form_submit_button("登录")

    if submitted:
        if authenticate(username, password, config):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("用户名或密码错误，请重新输入。")

    return False


@st.cache_resource(show_spinner=False)
def get_cached_vectorstore(
    file_names: tuple[str, ...],
    file_bytes: tuple[bytes, ...],
    persist_directory: str,
    collection_name: str,
):
    files = [
        UploadedPDF(name, data)
        for name, data in zip(file_names, file_bytes, strict=True)
    ]
    return build_vectorstore(
        files,
        persist_directory=persist_directory,
        collection_name=collection_name,
    )


def build_llm_client(api_key: str, model: str, base_url: str) -> OpenAICompatibleClient | None:
    if not api_key or not model or not base_url:
        return None
    return OpenAICompatibleClient(api_key=api_key, model=model, base_url=base_url)


def show_sources(docs) -> None:
    sources = build_sources(docs)
    if not sources:
        return

    with st.expander("查看检索来源", expanded=False):
        for source in sources:
            st.markdown(f"**片段 {source.index}**")
            st.write(source.content)


if not require_login():
    st.stop()

st.title("RAG Bot 2.0")

with st.sidebar:
    st.header("账号")
    if st.button("退出登录"):
        st.session_state["authenticated"] = False
        clear_messages(st.session_state)
        st.rerun()

    st.header("LLM")
    provider = st.selectbox("服务商", ["DeepSeek", "Groq", "OpenAI", "Custom OpenAI-Compatible"])
    env_api_key = get_env_api_key(provider)
    api_key = st.text_input(
        "API Key",
        value=env_api_key,
        type="password",
        help="可在页面输入，也可使用 DEEPSEEK_API_KEY / GROQ_API_KEY / OPENAI_API_KEY / OPENAI_COMPATIBLE_API_KEY 环境变量。",
    )
    model = st.text_input("模型", value=get_default_model(provider))
    base_url = st.text_input("Chat completions URL", value=get_default_base_url(provider))
    top_k = st.slider("检索片段数量", min_value=1, max_value=8, value=3)
    use_streaming = st.toggle("SSE 流式输出", value=True)

    st.header("历史记录")
    if st.button("清空历史"):
        clear_messages(st.session_state)
        st.rerun()

uploaded_files = st.file_uploader("上传 PDF", type=["pdf"], accept_multiple_files=True)

if not uploaded_files:
    st.info("请先上传一个或多个 PDF 文件。")
else:
    chroma_directory = get_default_chroma_directory()
    st.caption(f"Chroma 持久化目录：{chroma_directory}")

for message in get_messages(st.session_state):
    with st.chat_message(message["role"]):
        st.write(message["content"])

query = st.chat_input("输入你想问 PDF 的问题")

if query:
    if not uploaded_files:
        st.warning("请先上传 PDF，再开始提问。")
        st.stop()

    add_message(st.session_state, "user", query)
    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        try:
            names = tuple(file.name for file in uploaded_files)
            data = tuple(file.getvalue() for file in uploaded_files)
            collection_name = make_collection_name(names, data)
            vectorstore = get_cached_vectorstore(
                names,
                data,
                str(get_default_chroma_directory()),
                collection_name,
            )
            docs = vectorstore.similarity_search(query, k=top_k)
            llm_client = build_llm_client(api_key, model, base_url)

            if llm_client and use_streaming and docs:
                prompt = build_rag_prompt(query, docs)
                streamed_chunks: list[str] = []

                def stream_tokens():
                    for token in llm_client.generate_stream(prompt):
                        streamed_chunks.append(token)
                        yield token

                streamed_answer = st.write_stream(stream_tokens())
                answer_text = "".join(streamed_chunks) or str(streamed_answer)
                show_sources(docs)
                add_message(st.session_state, "assistant", answer_text)
            else:
                result = answer_question(query, docs, llm_client)
                if result.used_llm:
                    st.write(result.answer)
                else:
                    st.warning(result.answer)
                show_sources(docs)
                add_message(st.session_state, "assistant", result.answer)
        except Exception as exc:
            error_message = f"回答失败：{exc}"
            st.error(error_message)
            add_message(st.session_state, "assistant", error_message)
