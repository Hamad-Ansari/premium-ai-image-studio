# app.py
# PRO Free AI Image Generator (Clean + Fixed + Stylish)
# Streamlit + Hugging Face Free Models

import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="🎨 Free AI Image Generator",
    page_icon="🖼️",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b,#111827);
    color: white;
}

.title {
    font-size: 3.2rem;
    font-weight: 800;
    text-align: center;
    color: white;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 1.1rem;
    color: #cbd5e1;
    margin-bottom: 30px;
}

.stButton>button {
    background: linear-gradient(90deg,#8b5cf6,#ec4899);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 22px;
    font-size: 18px;
    font-weight: bold;
    width: 100%;
}

.stTextArea textarea, .stTextInput input {
    border-radius: 10px;
}

footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown('<div class="title">🎨 Free AI Image Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Create stunning images using FREE AI models</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("⚙️ Settings")

api_key = st.sidebar.text_input("🔑 Hugging Face API Key", type="password")

model = st.sidebar.selectbox(
    "🤖 Choose Model",
    [
        "black-forest-labs/FLUX.1-dev",
        "stabilityai/stable-diffusion-xl-base-1.0",
        "runwayml/stable-diffusion-v1-5"
    ]
)


# ---------------------------------------------------
# MAIN INPUTS
# ---------------------------------------------------
prompt = st.text_area(
    "✍️ Enter Prompt",
    height=150,
    placeholder="A futuristic city at sunset, neon lights, ultra realistic..."
)

negative_prompt = st.text_input(
    "🚫 Negative Prompt",
    placeholder="blurry, low quality, distorted"
)

# ---------------------------------------------------
# IMAGE GENERATOR
# ---------------------------------------------------
def generate_image(prompt):

    API_URL = f"https://router.huggingface.co/hf-inference/models/{model}"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return Image.open(BytesIO(response.content))

    else:
        st.error("❌ " + response.text)
        return None


# ---------------------------------------------------
# BUTTON
# ---------------------------------------------------
if st.button("✨ Generate Image"):

    if not api_key:
        st.warning("Please enter Hugging Face API Key")

    elif not prompt:
        st.warning("Please enter a prompt")

    else:
        with st.spinner("🎨 Creating masterpiece..."):

            final_prompt = prompt

            if negative_prompt:
                final_prompt += f", avoid {negative_prompt}"

            image = generate_image(final_prompt)

            if image:
                st.success("✅ Image Generated Successfully!")

                st.image(image, use_container_width=True)

                # Download
                buf = BytesIO()
                image.save(buf, format="PNG")

                st.download_button(
                    label="📥 Download Image",
                    data=buf.getvalue(),
                    file_name="ai_generated.png",
                    mime="image/png"
                )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("🚀 Built with Streamlit + Hugging Face Free Models")