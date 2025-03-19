import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(page_title="AI Image Editor", page_icon="🎨", layout="centered")

# Sidebar for API key input
st.sidebar.title("🔑 Settings")
st.sidebar.write("Enter your API key to use the service.")
api_key = st.sidebar.text_input("Google API Key", type="password")

# Main UI container
st.markdown("""
    <div style='max-width: 800px; margin: auto; text-align: center;'>
        <h1 style='color: #FF4B4B;'>🎨 AI-Powered Image Editor</h1>
        <p>Upload an image and describe how you want it modified!</p>
        <hr>
    </div>
    """, unsafe_allow_html=True)

# Initialize client only if API key is provided
if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.sidebar.warning("⚠️ Please enter a valid API key to proceed.")

# Centered content container
container = st.container()
with container:
    st.subheader("📤 Upload an Image")
    uploaded_file = st.file_uploader("Choose an image (JPG/PNG)", type=["jpg", "png"], help="Supported formats: JPG, PNG")

    st.subheader("📝 Describe the Modification")
    text_input = st.text_area("Enter your prompt:")

    # Display uploaded image
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

    # Button for generating image
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("✨ Generate Image", use_container_width=True)

# Generate modified image
if generate_btn:
    if not api_key:
        st.error("❌ API key is required!")
    elif uploaded_file is None:
        st.error("❌ Please upload an image first.")
    else:
        with st.spinner("⏳ Generating image..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp-image-generation",
                    contents=[text_input, image],
                    config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
                )
                
                for part in response.candidates[0].content.parts:
                    if part.text:
                        st.success("✅ AI Response:")
                        st.write(part.text)
                    elif part.inline_data:
                        result_image = Image.open(BytesIO(part.inline_data.data))
                        st.subheader("🖼️ Modified Image")
                        st.image(result_image, caption="Modified Image", use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("""
    <div style='max-width: 800px; margin: auto; text-align: center;'>
        <hr>
        <p style='font-size: 14px;'>Developed bY BuildFastWithAI with ❤️</p>
    </div>
    """, unsafe_allow_html=True)
