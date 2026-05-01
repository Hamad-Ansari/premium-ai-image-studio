# app.py
# PREMIUM AI Prompt Engine + Free Image Generator
# Streamlit App | No Complex Setup | Stylish UI

import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import urllib.parse

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="Premium AI Image Studio",
    page_icon="🎨",
    layout="wide"
)

# ------------------------------------------------
# CSS
# ------------------------------------------------
st.markdown("""
<style>
.stApp{
background: linear-gradient(135deg,#0f172a,#111827,#1e293b);
color:white;
}

.title{
font-size:3.4rem;
font-weight:800;
text-align:center;
margin-bottom:8px;
}

.subtitle{
text-align:center;
color:#cbd5e1;
font-size:1.1rem;
margin-bottom:30px;
}

.stButton>button{
background:linear-gradient(90deg,#8b5cf6,#ec4899);
color:white;
border:none;
border-radius:14px;
padding:12px 20px;
font-size:18px;
font-weight:700;
width:100%;
}

.block{
padding:18px;
border-radius:18px;
background:rgba(255,255,255,0.05);
backdrop-filter: blur(10px);
margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# HEADER
# ------------------------------------------------
st.markdown('<div class="title">🎨 Premium AI Image Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Prompt Engine + Free AI Image Generator</div>', unsafe_allow_html=True)

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------
st.sidebar.title("⚙️ Creative Controls")

style = st.sidebar.selectbox(
    "🎭 Style",
    [
        "Realistic Photography",
        "Cinematic",
        "Anime",
        "Fantasy Art",
        "Cyberpunk",
        "3D Render",
        "Digital Painting",
        "Portrait Studio"
    ]
)

ratio = st.sidebar.selectbox(
    "📐 Aspect Ratio",
    ["Square", "Landscape", "Portrait"]
)

quality = st.sidebar.selectbox(
    "💎 Quality",
    ["Standard", "High Detail", "Ultra"]
)

negative = st.sidebar.text_input(
    "🚫 Negative Prompt",
    "blurry, low quality, distorted, watermark, text"
)

# ------------------------------------------------
# MAIN INPUT
# ------------------------------------------------
user_prompt = st.text_area(
    "✍️ Describe Your Idea",
    height=180,
    placeholder="A futuristic city in rain at night..."
)

# ------------------------------------------------
# STYLE ENGINE
# ------------------------------------------------
style_map = {
    "Realistic Photography": "professional photography, ultra realistic, DSLR, natural lighting",
    "Cinematic": "cinematic lighting, dramatic mood, movie scene, depth of field",
    "Anime": "anime style, vibrant colors, detailed anime art, trending illustration",
    "Fantasy Art": "epic fantasy art, magical atmosphere, masterpiece concept art",
    "Cyberpunk": "cyberpunk neon lights, futuristic city, sci-fi atmosphere",
    "3D Render": "octane render, 3D CGI, hyper detailed render",
    "Digital Painting": "digital painting, brush textures, artstation quality",
    "Portrait Studio": "studio portrait, sharp focus, premium lighting, realistic skin"
}

quality_map = {
    "Standard": "high quality",
    "High Detail": "ultra detailed, sharp focus, rich textures",
    "Ultra": "8k, masterpiece, extremely detailed, ultra sharp, best quality"
}

ratio_map = {
    "Square": "1024x1024",
    "Landscape": "1280x768",
    "Portrait": "768x1280"
}

# ------------------------------------------------
# PROMPT ENGINE
# ------------------------------------------------
def build_prompt(text):
    final = f"""
{text},
{style_map[style]},
{quality_map[quality]},
beautiful composition,
professional color grading,
atmospheric lighting,
avoid {negative}
"""
    return " ".join(final.split())

# ------------------------------------------------
# FREE IMAGE API (Pollinations)
# ------------------------------------------------
def generate_image(prompt):
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}"

    response = requests.get(url)

    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    return None

# ------------------------------------------------
# BUTTONS
# ------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("⚡ Generate Smart Prompt"):

        if user_prompt:
            smart_prompt = build_prompt(user_prompt)

            st.markdown("### 🧠 Premium Prompt Output")
            st.code(smart_prompt, language="text")
        else:
            st.warning("Enter your idea first.")

with col2:
    if st.button("🎨 Generate Image"):

        if user_prompt:

            with st.spinner("Creating premium artwork..."):

                smart_prompt = build_prompt(user_prompt)
                image = generate_image(smart_prompt)

                if image:
                    st.success("✅ Image Generated!")

                    st.image(image, use_container_width=True)

                    buf = BytesIO()
                    image.save(buf, format="PNG")

                    st.download_button(
                        "📥 Download Image",
                        data=buf.getvalue(),
                        file_name="premium_ai_image.png",
                        mime="image/png"
                    )
                else:
                    st.error("Generation failed.")
        else:
            st.warning("Enter prompt first.")

# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.markdown("---")
st.caption("🚀 Built with Streamlit + Prompt Engine + Free AI Models")