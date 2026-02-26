import streamlit as st
import google.generativeai as genai
from PIL import Image

# 页面配置
st.set_page_config(page_title="AI 流程图转代码", layout="centered")

st.title("🖼️ 流程图 ➔ Mermaid 代码生成器")
st.write("上传图片，自动提取可编辑的代码，去 Draw.io 直接美化！")

# 侧边栏配置 API Key
with st.sidebar:
    st.header("设置")
    api_key = st.text_input("输入您的 Gemini API Key", type="password")
    st.info("Key 仅用于本次会话，不会被存储。")

# 上传组件
uploaded_file = st.file_uploader("请上传流程图照片 (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="待处理图片", use_container_width=True)
    
    if st.button("✨ 立即生成代码"):
        if not api_key:
            st.error("请先在左侧输入您的 API Key！")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                with st.spinner("AI 正在解析逻辑..."):
                    prompt = "识别图中流程图，严格输出 Mermaid 代码。包含 subgraph 和判断分支。只输出代码块，不要文字解释。"
                    response = model.generate_content([prompt, img])
                    
                    # 提取内容并清理标签
                    code = response.text.replace("```mermaid", "").replace("```", "").strip()
                    
                    st.success("解析成功！")
                    st.code(code, language="mermaid")
                    
                    # 添加跳转按钮
                    st.info("☝️ 复制上方代码后，点击下方按钮前往绘图：")
                    st.link_button("🚀 前往 Draw.io (Diagrams.net)", "https://app.diagrams.net/")
                    
            except Exception as e:
                st.error(f"解析出错：{e}")
