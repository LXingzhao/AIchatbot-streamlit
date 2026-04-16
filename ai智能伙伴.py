import streamlit as st
import os
from openai import OpenAI
from openai.resources.skills import content
from datetime import datetime
import json

#设置页面配置
st.set_page_config(
    page_title="AI智能伙伴",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

#保存会话信息的函数
def save_session():
    if st.session_state.current_session:
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }

        # 如果 sessions 文件夹不存在，则创建
        if not os.path.exists("sessions"):
            os.makedirs("sessions")

        # 保存会话数据
        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

#生成会话标识函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

#加载所有的会话列表信息
def load_sessions():
    session_list = []
    #加载sessions文件夹下所有的json文件
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True) # 倒序排列
    return session_list

#加载指定会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            # 加载会话数据
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_data["current_session"]
                st.session_state.messages = session_data["messages"]
    except Exception as e:
        st.error(f"加载会话信息失败：{e}")

#删除会话信息函数
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            #如果删除的是当前会话，则清空当前会话信息
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception as e:
        st.error(f"删除会话信息失败：{e}")

#大标题
st.title("AI智能伙伴")

#logo
st.logo("🤖", size="large")

#系统提示词
system_prompt="You are a helpful assistant"


#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

#昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = ""
#性格
if "nature" not in st.session_state:
    st.session_state.nature = ""
#会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()


#展示历史聊天信息
st.text(f"会话名称：{st.session_state.current_session}")
for message in st.session_state.messages: #{"role": "user", "content": prompt}
    if message["role"] == "user":
        st.chat_message("user", avatar="👨‍💻").write(message["content"])
    else:
        st.chat_message("assistant", avatar="🤖").write(message["content"])

#左侧侧边栏，with：python中的上下文管理器
with st.sidebar:
    #会话消息
    st.subheader("AI控制面板")

    #新建会话
    if st.button("新建会话",width="stretch",icon="💬"):

        #1、保存当前会话信息
        save_session()

        #2、创建新的会话
        if st.session_state.messages:   #如果聊天消息非空，True，否则False
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun()  # 重新运行页面，刷新会话信息

    #会话历史
    st.text("会话历史")
    session_list=load_sessions()
    for session in session_list:
        col1,col2=st.columns([4,1])
        with col1:
            # 点击历史会话，加载会话信息
            # 三元运算符,表达式：条件表达式 if 条件成立 else 条件不成立
            if st.button(session,width="stretch", icon="📃",key=f"load_{session}",type="primary" if session==st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()  # 重新运行页面，刷新会话信息
        with col2:
            # 删除历史会话
            if st.button("",width="stretch", icon="❌️",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()  # 重新运行页面，刷新会话信息


    #分割线
    st.divider()

    st.subheader("智能伙伴信息")
    #昵称输入框
    nick_name=st.text_input("昵称",placeholder="请输入昵称",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    #性格输入框
    nature=st.text_area("性格",placeholder="请输入性格",value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature


#聊天消息输入框
prompt=st.chat_input("请输入您要问的问题")
if prompt:                  #将LLM调用放入if语句中，防止页面刷新时调用LLM
    st.chat_message("user", avatar="👨‍💻").write(prompt)
    print( "---------->调用AI大模型，提示词：",prompt)

    #保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    #创建客户端（配置api-key）
    client = OpenAI(
        api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url="https://api.deepseek.com")


    #调用LLM
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            # 添加历史列表messages中的一个个字典message解包出来传给LLM，实现会话记忆功能
            *st.session_state.messages
        ],
        stream=True          # 开启流式返回
    )
    # 非流式输出LLM返回结果
    # print("<------------大模型返回结果：",response.choices[0].message.content)
    # #大模型回复
    # st.chat_message("assistant", avatar="🤖").write(response.choices[0].message.content)

    # 流式输出LLM返回结果
    response_message=st.empty ()   # 创建一个空元素，用于显示大模型返回的结果

    full_response=""
    for chunk in response:   # 大模型返回的流式数据
        if chunk.choices[0].delta.content is not None:
            content=chunk.choices[0].delta.content
            full_response+=content
            # 大模型回复
            response_message.chat_message("assistant", avatar="🤖").write(full_response)



    #保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # 保存当前会话信息
    save_session()