# AI智能伙伴 🤖
  基于 Streamlit + 大模型 API 开发的智能对话助手，支持多会话管理、角色设定、流式输出、历史记录自动保存。

## 1. 功能介绍
- 智能 AI 对话，支持上下文记忆
- 自定义 AI 昵称与性格
- 多会话管理：新建、切换、删除会话
- 会话历史自动保存到本地 JSON 文件
- 大模型流式输出，打字机效果
- 简洁美观的 Web 界面
- ![项目运行界面](images/项目运行示例.jpg)

## 2. 技术栈
- Python
- Streamlit
- OpenAI SDK
- DeepSeek 大模型 API
- JSON 本地存储会话

## 3. 安装依赖
```bash
pip install streamlit
pip install openai
```

## 4. 配置 API Key
   请注意，本人是在deepseek开放平台申请的api key，若使用者有其他api，可以参照对应平台说明文档使用自己的key复现该项目。
### 4.1 在电脑的环境变量中设置
```plaintext
DEEPSEEK_API_KEY=你的API密钥
```
### 4.2 直接在代码中填写
```python
client = OpenAI(
    api_key="你的API密钥",
    base_url="https://api.deepseek.com"
```
## 5. 运行项目
```bash
streamlit run ai智能伙伴.py
```

## 6. 项目结构
```plaintext
AI智能伙伴/
├── ai智能伙伴.py       # 主程序
├── sessions/           # 会话历史保存目录
├── README.md           # 项目说明
```
