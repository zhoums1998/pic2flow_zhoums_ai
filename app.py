import streamlit as st
import google.generativeai as genai
from PIL import Image

# 页面配置
st.set_page_config(page_title="AI 流程图转代码", layout="centered")
st.title("🖼️ 流程图 ➔ Mermaid 代码生成器")

with st.sidebar:
    st.header("设置")
    api_key = st.text_input("输入您的 Gemini API Key", type="password")
    st.info("检测到您的账号支持 Gemini 2.5 系列模型。")

uploaded_file = st.file_uploader("请上传流程图照片", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="图片已加载", use_container_width=True)
    
    if st.button("✨ 立即生成代码"):
        if not api_key:
            st.error("请先在左侧输入 API Key！")
        else:
            try:
                # 配置 API
                genai.configure(api_key=api_key)
                
                # --- 关键修改：精准匹配你账号中的 Gemini 2.5 Flash ---
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                with st.spinner("正在使用最新的 Gemini 2.5 Flash 解析逻辑..."):
                    prompt = "识别图中流程图，严格输出 Mermaid 代码。只输出代码块，不要任何文字解释。"
                    response = model.generate_content([prompt, img])
                    
                    if response.text:
                        # 清理 Markdown 标签
                        code = response.text.replace("```mermaid", "").replace("```", "").strip()
                        
                        st.success("解析成功！")
                        st.code(code, language="mermaid")
                        
                        st.info("☝️ 第一步：点击上方代码块右上角的图标进行复制")
                        st.link_button("🚀 第二步：前往 Draw.io 粘贴", "https://app.diagrams.net/")
                    else:
                        st.warning("AI 响应成功但未提取到内容。")
                        
            except Exception as e:
                # 如果 2.5 依然报错，提示用户检查权限
                st.error(f"发生错误：{str(e)}")
                st.info("请确保您在 AI Studio 看到的模型名称与代码一致。")
