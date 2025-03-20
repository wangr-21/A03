# 智能备课助手

## 开发配置

建议使用 `VS Code` 打开项目，`.vscode/` 中已配置相关插件和调试选项

其他 IDE 请自行配置项目

### 后端配置

- 运行如下命令安装 `uv`

```sh
# macOS / Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

- 在项目根目录下执行 `uv sync -p 3.12` 安装后端依赖

### 前端配置

- 安装 [node.js](https://nodejs.org/zh-cn)
- 在项目根目录下执行 `npm i` 安装前端依赖

### 调试配置

- 在项目根目录下创建 `.env` 文件，填写 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`

```env
OPENAI_API_KEY=sk-xxxxxx
OPENAI_BASE_URL=https://xxxxxx/v1
```

- 在 `VS Code` 侧边 `调试` 栏中选择 `全栈: 启动前端+后端`，`F5` 启动调试
- 后端输出位于 `VSC` 下方 `终端` 页，前端输出位于 `调试控制台` 页
- 默认前端地址为 http://localhost:5173/
