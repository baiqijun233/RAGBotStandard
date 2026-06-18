# 开发困难与升级总结

## 背景

本项目来自前序 ChatGPT 对话中的 PDF RAG 学习过程。早期目标是做一个可以上传 PDF、切分文本、建立向量库并根据问题检索内容的 Streamlit 应用。后续升级目标是把它从“PDF 检索器”推进到“真正能回答问题的 RAG Bot”。

本轮 2026-06-18 继续升级：

```text
登录 -> 上传 PDF -> Chroma 持久化 -> 检索片段 -> 组装 Prompt -> LLM 流式或非流式回答 -> 保存本轮历史
```

## 你在前序开发中遇到的问题

### 1. Python 环境和依赖混乱

表现：
- `.venv` 是否激活不清楚。
- `langchain_community` 找不到。
- 安装依赖的 Python 和运行项目的 Python 不一致。

原因：
- Windows 上系统 Python、虚拟环境、编辑器解释器容易混用。
- LangChain 拆分后依赖包变多，需要同时安装 `langchain-community`、`langchain-core`、`langchain-text-splitters`、`langchain-chroma` 等。

改进：
- 统一在 `02_Source/rag-bot-standard` 内使用 `.venv`。
- 依赖统一写入 `requirements.txt`。
- 测试命令统一使用 `.\.venv\Scripts\python.exe`。

### 2. Streamlit 页面看起来像空白

表现：
- 终端显示 `Local URL: http://localhost:8501`，但浏览器页面信息很少。
- 不确定应该在终端输入问题，还是在网页输入问题。

原因：
- Streamlit 的交互发生在浏览器页面。
- 早期页面状态提示不足，未上传 PDF 时用户不知道下一步做什么。

改进：
- 页面增加登录、上传提示、聊天输入框。
- 没上传 PDF 时给出明确提示。
- 上传 PDF 后显示 Chroma 数据目录，便于确认数据没有散落到其他位置。

### 3. LangChain API 变化

表现：

```text
AttributeError: 'VectorStoreRetriever' object has no attribute 'get_relevant_documents'
```

原因：
- 新版 LangChain 的 retriever 接口发生变化，旧的 `get_relevant_documents()` 不再适合继续依赖。

改进：
- 主流程改为 `vectorstore.similarity_search(query, k=top_k)`。
- 测试重点放在本项目自己的封装函数，降低外部 API 变化对项目理解的干扰。

### 4. 初始化顺序错误

表现：

```text
NameError: name 'vectorstore' is not defined
```

原因：
- 在上传 PDF 并创建 `vectorstore` 之前，就提前调用了向量检索相关逻辑。
- Streamlit 每次交互都会从上到下重跑脚本，变量初始化顺序很重要。

改进：
- 只有上传 PDF 后才创建向量库。
- 只有用户提问后才执行检索和回答。
- 使用 `st.cache_resource` 缓存向量库构建结果。

### 5. 只显示原文片段，不是真正 RAG

表现：

```python
st.write(docs[0].page_content)
```

这只能显示一个检索片段，不能综合多个片段生成答案。

改进：
- 新增 `rag_bot/rag_answering.py` 组装中文 RAG Prompt。
- 新增 `rag_bot/llm_client.py` 接入 OpenAI 兼容接口。
- 没有 API Key 时降级展示检索依据，不直接崩溃。

## 我本轮实际改造中遇到的问题

### 1. 中文乱码影响源码和文档可读性

表现：
- 之前生成的部分 README、工作台、验证日志和提示词出现中文乱码。
- 页面帮助文字和模型系统提示词也有乱码风险。

原因：
- Windows PowerShell 控制台编码和文件 UTF-8 显示之间容易混乱。
- 局部补丁匹配乱码上下文时不稳定。

处理：
- 对关键文档和小源码文件采用整文件整理。
- 保持文件内容为正常 UTF-8 中文。
- 将这个问题记录为本轮不足，后续写中文文档时要及时打开验证。

### 2. TDD 红灯阶段出现测试写法错误

表现：
- SSE 测试里最初使用了包含中文的 bytes 字面量，Python 报错：

```text
SyntaxError: bytes can only contain ASCII literal characters
```

原因：
- Python 的 bytes 字面量只能直接写 ASCII 字符。

处理：
- 改成普通字符串再 `.encode("utf-8")`。
- 重新运行测试，确认红灯原因变成“功能未实现”，再继续写生产代码。

### 3. Chroma 持久化不能只写目录

问题：
- 只设置 `persist_directory` 虽然能持久化，但如果集合命名和片段 ID 不稳定，重启后可能产生重复数据或混入不同 PDF 的内容。

处理：
- `make_collection_name()` 根据上传文件名和文件内容生成稳定集合名。
- `make_chunk_ids()` 根据集合名、片段序号和片段内容生成稳定 ID。
- Chroma 数据固定放在 `Project001_RAGBotStandard\04_Data\chroma`。

### 4. 登录只能先做轻量版本

问题：
- 用户要求“登录”，但当前是本地 Streamlit 应用，没有数据库和用户系统。

处理：
- 先实现本地轻量门禁，默认 `admin / ragbot`。
- 支持通过环境变量 `RAG_BOT_USERNAME`、`RAG_BOT_PASSWORD` 修改。
- 文档明确说明：这不是企业级账号系统，只适合本地测试或轻量访问控制。

### 5. SSE 流式输出依赖服务商兼容程度

问题：
- DeepSeek、Groq、OpenAI 都偏 OpenAI 兼容，但流式返回细节可能有差异。

处理：
- 解析标准 `data: {...}` 和 `data: [DONE]`。
- 遇到非 JSON 流式片段会抛出明确错误。
- 页面保留流式开关，必要时可以切回普通一次性回答。

## 本轮新增文件

- `02_Source/rag-bot-standard/rag_bot/auth.py`：登录配置和校验。
- `02_Source/rag-bot-standard/rag_bot/chat_history.py`：聊天历史读写和清空。
- `02_Source/rag-bot-standard/tests/test_auth.py`：登录测试。
- `02_Source/rag-bot-standard/tests/test_chat_history.py`：历史记录测试。

## 本轮重点修改文件

- `02_Source/rag-bot-standard/app.py`：整合登录、历史、SSE、Chroma 持久化。
- `02_Source/rag-bot-standard/rag_bot/llm_client.py`：增加流式请求和 SSE 解析。
- `02_Source/rag-bot-standard/rag_bot/vectorstore.py`：增加项目内 Chroma 目录、集合名、片段 ID。
- `02_Source/rag-bot-standard/rag_bot/rag_answering.py`：修复中文提示词乱码。
- `02_Source/rag-bot-standard/README.md`：重写为新版使用说明。
- `05_Docs/Project_Architecture_Analysis.html`：更新为网页版架构解析。

## 当前边界和后续改进

- 历史记录只保存在 Streamlit 会话里，不会跨服务重启长期保存。
- 登录是本地轻量版本，后续如要多人使用，需要接数据库或正式认证系统。
- Chroma 已持久化到项目内，但后续还可以增加“已存在集合直接复用”的更细控制。
- 尚未使用真实 DeepSeek/Groq/OpenAI Key 做端到端回答验证。
- 如果继续扩大项目，建议先补更多测试，再加数据库、文件管理、用户管理等功能。
