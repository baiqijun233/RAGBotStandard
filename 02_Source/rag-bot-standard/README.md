# RAG Bot Standard

这是 Project001 的清理升级版 PDF RAG 项目。它可以上传 PDF，提取文本，切分片段，写入 Chroma 向量库，再把检索到的内容交给 DeepSeek、Groq、OpenAI 或其他 OpenAI 兼容接口生成中文回答。

## 当前已完成能力

- PDF 上传和文本提取
- 文本切分和向量检索
- Chroma 持久化，数据目录固定在项目内的 `04_Data/chroma`
- DeepSeek、Groq、OpenAI、自定义 OpenAI 兼容接口
- API Key 页面输入或环境变量读取
- 登录页，本地默认账号 `admin`，默认密码 `ragbot`
- 聊天历史记录，使用 Streamlit 会话状态保存
- SSE 流式输出，服务商支持时可以边生成边显示
- 未配置 API Key 时自动降级为“只显示检索依据”

## 项目结构

```text
Project001_RAGBotStandard/
  00_Project_Workbench/
  01_Requirements/
  02_Source/
    rag-bot-standard/
      app.py
      rag_bot/
        auth.py
        chat_history.py
        llm_client.py
        pdf_loader.py
        rag_answering.py
        vectorstore.py
      tests/
  03_Assets/
  04_Data/
    chroma/
  05_Docs/
  06_Tests/
  07_Logs/
  08_Deliverables/
```

## 启动方式

```powershell
cd E:\Agent\AIProjects\Project001_RAGBotStandard\02_Source\rag-bot-standard
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

如果虚拟环境不可用，重新创建：

```powershell
cd E:\Agent\AIProjects\Project001_RAGBotStandard\02_Source\rag-bot-standard
C:\Users\aeocbaiqijun\AppData\Local\Programs\Python\Python311\python.exe -m venv .venv --clear
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

浏览器通常打开：

```text
http://localhost:8501
```

## 登录配置

本地测试默认：

```text
用户名：admin
密码：ragbot
```

正式使用前建议改成环境变量：

```powershell
$env:RAG_BOT_USERNAME="你的用户名"
$env:RAG_BOT_PASSWORD="你的强密码"
```

## LLM 配置

DeepSeek：

```powershell
$env:DEEPSEEK_API_KEY="你的 DeepSeek Key"
```

Groq：

```powershell
$env:GROQ_API_KEY="你的 Groq Key"
```

OpenAI：

```powershell
$env:OPENAI_API_KEY="你的 OpenAI Key"
```

自定义 OpenAI 兼容接口：

```powershell
$env:OPENAI_COMPATIBLE_API_KEY="你的 Key"
$env:OPENAI_COMPATIBLE_BASE_URL="https://example.com/v1/chat/completions"
$env:OPENAI_COMPATIBLE_MODEL="模型名"
```

## Chroma 数据位置

向量库数据固定放在：

```text
E:\Agent\AIProjects\Project001_RAGBotStandard\04_Data\chroma
```

集合名会根据上传 PDF 的文件名和文件内容生成，片段 ID 也会稳定生成，避免同一批文件在同一集合里反复写入大量重复片段。

## 测试命令

```powershell
cd E:\Agent\AIProjects\Project001_RAGBotStandard\02_Source\rag-bot-standard
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall app.py rag_bot tests
```

## 重要边界

- 历史记录当前只保存在本次浏览器会话里，刷新服务或退出登录后会丢失。
- 登录是本地轻量门禁，不是企业级账号系统。
- SSE 流式输出依赖服务商接口支持 `stream: true`。
- 没有 API Key 时不会调用大模型，只会展示 PDF 检索依据。
