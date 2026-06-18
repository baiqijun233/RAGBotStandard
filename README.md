# RAGBotStandard

一个面向面试展示的本地 AI 项目：基于 Streamlit、LangChain 和 Chroma，实现 PDF 上传、向量检索、RAG 问答、DeepSeek/OpenAI 兼容模型接入、SSE 流式输出、登录和历史记录。

## 项目亮点

- 支持 PDF 上传、文本提取、分块切分和向量化检索
- 使用 Chroma 做本地持久化向量库，数据存放在项目目录内
- 支持 DeepSeek、OpenAI、Groq 和自定义 OpenAI 兼容接口
- 支持 SSE 流式输出，回答可以边生成边展示
- 支持本地登录和会话级历史记录
- 包含单元测试、验证日志、迁移说明和架构解析文档

## 适合面试讲什么

这个项目不只是一个“跑通教程”的 Demo，而是一个做过整理和升级的 RAG 项目，适合展示这些能力：

- 如何把 PDF 文档转成可检索的知识库
- RAG 检索链路是怎么工作的
- 如何把大模型接入到本地网页应用
- 如何处理登录、历史记录、流式输出和持久化这些工程问题
- 如何把一个零散项目迁移成可维护的标准项目结构

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

## 快速启动

```powershell
cd E:\Agent\AIProjects\Project001_RAGBotStandard\02_Source\rag-bot-standard
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

浏览器打开：

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
- 当前更适合本地演示、学习和面试展示，不是直接上线的生产版本
