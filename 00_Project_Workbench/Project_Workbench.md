# Project001_RAGBotStandard 工作台

## 项目目标

把早期 PDF RAG 学习项目整理成正式编号项目，并升级成可登录、可保留会话历史、可使用 Chroma 持久化、可接入 DeepSeek/Groq/OpenAI 的 Streamlit RAG Bot。

## 当前状态

- 状态：RAG Bot 2.0 已完成本轮功能升级，等待真实 API Key 和真实 PDF 进一步端到端联调。
- 最近更新时间：2026-06-18
- 项目根目录：`E:\Agent\AIProjects\Project001_RAGBotStandard`
- 主源码目录：`E:\Agent\AIProjects\Project001_RAGBotStandard\02_Source\rag-bot-standard`
- 旧版参考目录：`E:\Agent\AIProjects\Project001_RAGBotStandard\02_Source\rag-rag2-legacy`
- 项目文档目录：`E:\Agent\AIProjects\Project001_RAGBotStandard\05_Docs`
- 验证日志目录：`E:\Agent\AIProjects\Project001_RAGBotStandard\07_Logs`

## 本轮关键改动

- 新增登录门禁：默认 `admin / ragbot`，正式使用可通过 `RAG_BOT_USERNAME` 和 `RAG_BOT_PASSWORD` 修改。
- 新增历史记录：用 Streamlit 会话状态保存本轮对话，可清空，可退出登录时清理。
- 新增 SSE 流式输出：LLM 客户端支持解析 OpenAI 兼容的 `data: ...` 流式响应。
- 强化 Chroma：向量库固定写入项目内 `04_Data/chroma`，集合名和片段 ID 根据 PDF 内容稳定生成。
- 修复中文乱码：源码提示词、界面文案、README 和项目文档重新整理为正常中文。
- 补充测试：新增登录、历史记录、SSE、Chroma 持久化相关单元测试。

## 启动方式

```powershell
cd E:\Agent\AIProjects\Project001_RAGBotStandard\02_Source\rag-bot-standard
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

如果 `.venv` 因迁移或路径变化不可用：

```powershell
cd E:\Agent\AIProjects\Project001_RAGBotStandard\02_Source\rag-bot-standard
C:\Users\aeocbaiqijun\AppData\Local\Programs\Python\Python311\python.exe -m venv .venv --clear
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## 关键决策

- 2026-06-17：项目正式编号为 `Project001_RAGBotStandard`。
- 2026-06-17：清理版 `rag-bot-standard` 作为主源码，旧版 `rag-rag2` 只保留为 legacy 参考。
- 2026-06-17：所有相关内容必须放在 Project001 项目目录内，不能散落到 `AIProjects` 根目录或电脑其他位置。
- 2026-06-17：全局规则文档保持少量集中，避免过度拆分。
- 2026-06-18：历史记录、SSE、Chroma 持久化、登录纳入主项目，不另开新项目。

## 待办事项

- [x] 迁移到标准编号项目目录。
- [x] 升级为真正的 LLM RAG 回答流程。
- [x] 兼容 DeepSeek。
- [x] 增加历史记录。
- [x] 增加 SSE 流式输出。
- [x] 增加 Chroma 项目内持久化。
- [x] 增加登录门禁。
- [x] 更新网页版项目解析文档。
- [ ] 使用真实 API Key 和真实 PDF 做端到端联调。
- [ ] 后续如需长期保存聊天历史，可再接入本地数据库或 JSONL 记录。
