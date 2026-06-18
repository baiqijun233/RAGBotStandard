from dataclasses import dataclass
from typing import Protocol


class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...


@dataclass(frozen=True)
class SourceSnippet:
    index: int
    content: str
    metadata: dict


@dataclass(frozen=True)
class RAGAnswer:
    answer: str
    sources: list[SourceSnippet]
    used_llm: bool


def build_sources(docs) -> list[SourceSnippet]:
    return [
        SourceSnippet(
            index=index,
            content=getattr(doc, "page_content", "").strip(),
            metadata=getattr(doc, "metadata", {}) or {},
        )
        for index, doc in enumerate(docs, start=1)
        if getattr(doc, "page_content", "").strip()
    ]


def build_rag_prompt(question: str, docs) -> str:
    sources = build_sources(docs)
    context = "\n\n".join(
        f"[片段 {source.index}]\n{source.content}"
        for source in sources
    )

    return f"""你是一个严谨的 PDF 问答助手。
请只根据下面提供的 PDF 内容回答问题。如果内容不足以回答，请明确说“文档中没有足够信息”。请用中文回答，先给出直接答案，再用简短要点说明依据。
PDF 内容：
{context}

用户问题：
{question}
"""


def answer_question(question: str, docs, llm_client: LLMClient | None = None) -> RAGAnswer:
    sources = build_sources(docs)

    if not sources:
        return RAGAnswer(
            answer="没有检索到相关 PDF 内容，请确认 PDF 可读取，或换一个更具体的问题。",
            sources=[],
            used_llm=False,
        )

    if llm_client is None:
        return RAGAnswer(
            answer=(
                "已检索到相关内容，但未配置 LLM，所以当前只显示检索依据。"
                "配置 API Key 后即可生成真正的 AI 总结回答。"
            ),
            sources=sources,
            used_llm=False,
        )

    prompt = build_rag_prompt(question, docs)
    return RAGAnswer(
        answer=llm_client.generate(prompt).strip(),
        sources=sources,
        used_llm=True,
    )
