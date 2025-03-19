import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Sidebar for API key input
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter Google API Key", type="password")

# Streamlit UI
st.title("🎨 AI-Powered Image Editor with Google GenAI")
st.write("Upload an image and describe how you want it modified!")

# Initialize client only if API key is provided
if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.sidebar.warning("Please enter a valid API key to proceed.")

# Upload image
uploaded_file = st.file_uploader("Upload an image (JPG/PNG)", type=["jpg", "png"])

# Text input for modification
text_input = st.text_area("Enter a prompt to modify the image:", "Change the color of the clothes of PM Modi to yellow")

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Generate modified image
if st.button("Generate Image"):
    if not api_key:
        st.error("API key is required!")
    elif uploaded_file is None:
        st.error("Please upload an image first.")
    else:
        with st.spinner("Generating image..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp-image-generation",
                    contents=[text_input, image],
                    config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
                )
                
                for part in response.candidates[0].content.parts:
                    if part.text:
                        st.write(part.text)
                    elif part.inline_data:
                        result_image = Image.open(BytesIO(part.inline_data.data))
                        st.image(result_image, caption="Modified Image", use_container_width=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
