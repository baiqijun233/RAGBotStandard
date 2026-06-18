# 迁移说明

## 迁移结果

正式项目目录：

```text
E:\Agent\AIProjects\Project001_RAGBotStandard
```

清理版源码：

```text
E:\Agent\AIProjects\Project001_RAGBotStandard\02_Source\rag-bot-standard
```

旧版原始项目：

```text
E:\Agent\AIProjects\Project001_RAGBotStandard\02_Source\rag-rag2-legacy
```

## 已完成整理

- 创建正式编号项目文件夹 `Project001_RAGBotStandard`。
- 创建标准子目录：`00_Project_Workbench` 到 `08_Deliverables`。
- 将清理版源码放入 `02_Source/rag-bot-standard`。
- 将旧版项目保留在 `02_Source/rag-rag2-legacy`，作为参考，不再作为主项目运行入口。
- 将项目说明、问题总结、网页解析文档放入 `05_Docs`。
- 将验证记录放入 `07_Logs`。
- 将 Chroma 持久化数据固定放入 `04_Data/chroma`。

## 本轮升级并入情况

2026-06-18 的功能升级没有另开新项目，而是直接并入 Project001：

- 登录：`rag_bot/auth.py`
- 历史记录：`rag_bot/chat_history.py`
- SSE 流式输出：`rag_bot/llm_client.py`
- Chroma 持久化：`rag_bot/vectorstore.py`
- 页面入口整合：`app.py`
- 新增测试：`tests/test_auth.py`、`tests/test_chat_history.py`、`tests/test_llm_client.py`、`tests/test_vectorstore.py`

## 后续注意

以后不要直接在 `E:\Agent\AIProjects` 根目录创建无编号项目文件夹。每个项目必须先创建：

```text
ProjectNNN_ProjectName
```

并且所有源码、数据、文档、日志、交付物都要放入对应项目文件夹。
