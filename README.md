# RAGBotStandard

An interview-ready local AI project built with Streamlit, LangChain, and Chroma. It supports PDF upload, vector retrieval, RAG question answering, DeepSeek and OpenAI-compatible model integration, SSE streaming output, login, and chat history.

一个本地运行的 PDF RAG 项目，基于 Streamlit、LangChain 和 Chroma，实现 PDF 上传、向量检索、RAG 问答、DeepSeek/OpenAI 兼容模型接入、SSE 流式输出、登录和历史记录。

## 项目亮点

- 支持 PDF 上传、文本提取、分块切分和向量化检索
- 使用 Chroma 做本地持久化向量库，数据存放在项目目录内
- 支持 DeepSeek、OpenAI、Groq 和自定义 OpenAI 兼容接口
- 支持 SSE 流式输出，回答可以边生成边展示
- 支持本地登录和会话级历史记录
- 包含单元测试、验证日志、迁移说明和架构解析文档

## 项目价值

这个项目围绕本地知识问答场景进行了完整实现和工程化整理，适合作为 RAG 项目的展示样例。它覆盖了文档处理、向量检索、大模型接入、流式输出、登录控制、历史记录和项目结构标准化等关键环节。

它重点体现这些能力：

- 将 PDF 文档转换为可检索的本地知识库
- 构建从检索到生成的 RAG 问答链路
- 将大模型能力接入到本地网页应用
- 处理登录、历史记录、流式输出和持久化等工程问题
- 将零散原型整理为可维护的标准项目结构

## 技术栈

- `Python`
- `Streamlit`
- `LangChain`
- `Chroma`
- `HuggingFace Embeddings`
- `DeepSeek / OpenAI-compatible API`

## 当前功能

- PDF 上传
- 文本切分
- 向量检索
- RAG 问答
- DeepSeek 兼容接入
- SSE 流式输出
- 本地登录
- 历史记录
- Chroma 持久化
- 单元测试

## 项目结构

```text
Project001_RAGBotStandard/
  00_Project_Workbench/
  01_Requirements/
  02_Source/
    rag-bot-standard/
  03_Assets/
  04_Data/
  05_Docs/
  06_Tests/
  07_Logs/
  08_Deliverables/
```

主程序入口：

```text
02_Source/rag-bot-standard/app.py
```

## 运行方式

```powershell
cd E:\Agent\AIProjects\Project001_RAGBotStandard\02_Source\rag-bot-standard
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

访问地址：

```text
http://localhost:8501
```

## 默认登录信息

本地测试默认账号：

```text
用户名：admin
密码：ragbot
```

正式使用前可以通过环境变量覆盖：

```powershell
$env:RAG_BOT_USERNAME="your_username"
$env:RAG_BOT_PASSWORD="your_password"
```

## 文档入口

- 项目源码说明：[02_Source/rag-bot-standard/README.md](./02_Source/rag-bot-standard/README.md)
- 架构解析：[05_Docs/Project_Architecture_Analysis.html](./05_Docs/Project_Architecture_Analysis.html)
- 迁移说明：[05_Docs/Migration_Summary.md](./05_Docs/Migration_Summary.md)
- 开发困难总结：[05_Docs/Development_Difficulties_and_Upgrade_Summary.md](./05_Docs/Development_Difficulties_and_Upgrade_Summary.md)
- 验证日志：[07_Logs/Verification_Log.md](./07_Logs/Verification_Log.md)

## 当前边界

- 历史记录目前只保存在当前会话内，不是长期数据库存储
- 登录是本地轻量门禁，不是完整用户系统
- 真实大模型端到端演示仍需要配置可用的 API Key
- 当前更适合本地演示、学习和项目展示，不是直接上线的生产版本
