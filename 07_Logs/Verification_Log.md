# 验证日志

## 2026-06-17 初次迁移验证

验证目标：
- 确认项目已经进入正式编号目录。
- 确认 `AIProjects` 根目录不再散落无编号 RAG 项目。

关键结果：

```text
Project001_RAGBotStandard
```

## 2026-06-17 RAG 2.0 升级验证

执行目录：

```text
E:\Agent\AIProjects\Project001_RAGBotStandard\02_Source\rag-bot-standard
```

执行：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall app.py rag_bot tests
Invoke-WebRequest -UseBasicParsing http://localhost:8501
```

关键结果：

```text
Ran 8 tests in 0.001s
OK
HTTP 200
```

未完成验证：
- 当时未使用真实 `DEEPSEEK_API_KEY`、`GROQ_API_KEY` 或 `OPENAI_API_KEY` 做端到端 LLM 联调。

## 2026-06-18 登录、历史记录、SSE、Chroma 持久化升级验证

执行目录：

```text
E:\Agent\AIProjects\Project001_RAGBotStandard\02_Source\rag-bot-standard
```

### 1. 单元测试

执行：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

结果：

```text
Ran 19 tests in 0.007s
OK
```

覆盖内容：
- 登录默认配置、环境变量配置、用户名密码校验。
- 聊天历史追加、清空、空内容拦截。
- DeepSeek、Groq、OpenAI 默认配置。
- OpenAI 兼容 SSE 流式内容解析和异常处理。
- PDF 文本切分。
- RAG Prompt 和无 LLM 降级回答。
- Chroma 项目内目录、集合名、片段 ID 稳定性。

### 2. Python 编译检查

执行：

```powershell
.\.venv\Scripts\python.exe -m compileall app.py rag_bot tests
```

结果：

```text
Compiling 'app.py'...
Listing 'rag_bot'...
Listing 'tests'...
```

结论：入口、模块和测试文件语法检查通过。

### 3. Streamlit HTTP 检查

执行：

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8501 -TimeoutSec 10
```

结果：

```text
HTTP 200 OK
```

### 4. Playwright 页面检查

执行：

```powershell
npx --yes --package @playwright/cli playwright-cli open http://127.0.0.1:8501
npx --yes --package @playwright/cli playwright-cli snapshot
npx --yes --package @playwright/cli playwright-cli fill e70 admin
npx --yes --package @playwright/cli playwright-cli fill e78 ragbot
npx --yes --package @playwright/cli playwright-cli click e84
npx --yes --package @playwright/cli playwright-cli snapshot
```

验证结果：
- 登录页标题正常：`RAG Bot 2.0 登录`。
- 默认登录提示正常显示：`admin / ragbot`。
- 用户名、密码输入框和登录按钮可见。
- 使用默认账号登录后进入主页面。
- 主页面可见：LLM 配置、DeepSeek 默认模型、DeepSeek 默认接口、SSE 流式输出开关、历史记录清空按钮、PDF 上传区、聊天输入框。

截图记录：

```text
E:\Agent\AIProjects\Project001_RAGBotStandard\07_Logs\ragbot_login_page_2026-06-18-second.png
```

### 5. 未完成或受限验证

- 尚未配置真实 `DEEPSEEK_API_KEY`、`GROQ_API_KEY` 或 `OPENAI_API_KEY`，所以没有执行真实大模型扣费接口调用。
- 尚未上传真实 PDF 做完整端到端问答验证。
- 历史记录当前是 Streamlit 会话级保存，未测试跨服务重启长期保存，因为本轮没有实现长期历史数据库。

## 2026-06-18 用户浏览器运行后检查

检查目标：
- 确认用户在浏览器中运行后，服务、页面和 Chroma 数据是否正常。

检查结果：

```text
HTTP 200 OK
```

Chroma 数据目录：

```text
E:\Agent\AIProjects\Project001_RAGBotStandard\04_Data\chroma
```

Chroma 集合检查：

```text
collections= ['rag_pdf_471b3ed449840ba2']
rag_pdf_471b3ed449840ba2 5
```

页面检查：
- 当前页面标题为 `RAG Bot 2.0`。
- 已进入主页面，能看到 LLM 设置、DeepSeek 默认配置、SSE 流式输出开关、上传 PDF 区和聊天输入框。
- 浏览器控制台出现过短暂 `ERR_NETWORK_IO_SUSPENDED`，但后续 `_stcore/health` 和 `_stcore/host-config` 均恢复为 200，未发现业务级页面错误。

注意事项：
- 当前检测到两个 Streamlit 相关 Python 进程，其中 8501 端口由系统 Python 进程提供服务，不是项目 `.venv` 进程。
- 面试演示前建议关闭多余进程，只用项目 `.venv` 重新启动，避免环境混乱。

## 2026-06-18 关闭浏览器后的复测

用户关闭浏览器后再次检查：

```text
HTTP 200 OK
```

Chroma 持久化数据仍然存在：

```text
collections= ['rag_pdf_471b3ed449840ba2']
rag_pdf_471b3ed449840ba2 5
```

进程检查结果：
- 仍检测到两个 Streamlit 相关 Python 进程。
- `8501` 端口仍由系统 Python 进程提供服务。

结论：
- 关闭浏览器标签页不会关闭 Streamlit 后端服务。
- Chroma 数据已经持久化，关闭浏览器后不会丢失。
- 如果要做干净的面试演示，需要先停止旧 Streamlit 进程，再用项目 `.venv` 重新启动。
