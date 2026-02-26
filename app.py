import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 页面基本配置
st.set_page_config(page_title="AI 流程图转代码", layout="centered")

st.title("🖼️ 流程图 ➔ Mermaid 代码生成器")
st.write("上传图片，自动提取可编辑的代码，去 Draw.io 直接美化！")

# 2. 侧边栏配置 API Key
with st.sidebar:
    st.header("设置")
    api_key = st.text_input("输入您的 Gemini API Key", type="password")
    st.info("Key 仅用于本次会话，不会被存储。")

# 3. 主界面上传组件
uploaded_file = st.file_uploader("请上传流程图照片 (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="待处理图片预览", use_container_width=True)
    
    if st.button("✨ 立即生成代码"):
        if not api_key:
            st.error("请先在左侧输入您的 API Key！")
        else:
            try:
                # 配置 API，增加 transport 声明以提高云端稳定性
                genai.configure(api_key=api_key, transport='rest')
                
                # 使用最标准的模型全称，解决 404 models not found 问题
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                
                with st.spinner("AI 正在深度解析流程逻辑，请稍候..."):
                    prompt = "识别图中流程图，严格输出 Mermaid 代码。包含 subgraph 和判断分支。只输出代码块，不要任何文字解释。"
                    
                    # 发送请求
                    response = model.generate_content([prompt, img])
                    
                    # 检查是否有内容返回
                    if response and response.text:
                        # 清理可能存在的 Markdown 标签
                        code = response.text.replace("```mermaid", "").replace("```", "").strip()
                        
                        st.success("解析成功！")
                        st.code(code, language="mermaid")
                        
                        # 操作引导
                        st.info("☝️ 第一步：点击上方代码块右上角的图标进行复制")
                        st.link_button("🚀 第二步：前往 Draw.io (Diagrams.net) 粘贴", "https://app.diagrams.net/")
                    else:
                        st.warning("AI 响应成功但未提取到代码，请尝试换一张更清晰的图片。")
                        
            except Exception as e:
                # 捕获详细错误，方便我们后续排查
                error_str = str(e)
                if "404" in error_str:
                    st.error("错误 404：模型名称未找到。请确认你的 API Key 是否支持 Gemini 1.5 系列。")
                elif "403" in error_str:
                    st.error("错误 403：权限不足或 API Key 填错，请检查 Key 是否有效。")
                else:
                    st.error(f"发生意外错误：{error_str}")

# 底部小提示
st.divider()
st.caption("提示：如果生成的图形不完美，可以在 Draw.io 插入后手动微调方框位置。")
