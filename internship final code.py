
import streamlit as st
from PIL import Image
import pyttsx3
import os
import pytesseract  
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
import tempfile
from gtts import gTTS

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Initialize Google Generative AI with API Key
GEMINI_API_KEY = 'Google API Key'
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=GEMINI_API_KEY)

# Streamlit Page Configurations
st.set_page_config(page_title="Visually Impaired Assistant", layout="wide", page_icon="🧠")

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        color: #444;
        text-align: center;
        margin-bottom: 30px;
    }
    .card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .card h3 {
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown('<div class="main-title">Visually Impaired Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Solutions for Accessibility</div>', unsafe_allow_html=True)

# Sidebar Features
st.sidebar.image(r"C:\Users\Akhil Reddy\Downloads\img.png", width=250)
st.sidebar.title("ℹ️ About")
st.sidebar.markdown(
    """
    ### 🌟 Highlighted Features
    
🖼️ scene description
    Convert visuals into meaningful descriptions, capturing key elements and actions.
📄 Text extraction
  Effortlessly detect and retrieve text from any uploaded image.
🎧 speech extraction
Transform text into speech for an engaging audio experience.


    ### 🤖 Technology Behind
    
🌐 Google Gemini API: Advanced AI for smart scene understanding.
🔍 Tesseract OCR: Reliable tool for precise text extraction.
🎙️ Speech Technology: Delivers natural-sounding text-to-speech conversion.
"""
)

# Utility Functions
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def text_to_speech(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts = gTTS(text=text, lang="en")
        tts.save(temp_audio.name)
        return temp_audio.name

def generate_scene_description(input_prompt, image_data):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

def prepare_image_data(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    return [{"mime_type": uploaded_file.type, "data": bytes_data}]

# Main Content
st.markdown("<div class='card'><h3>1. Upload an Image</h3></div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    st.markdown("<div class='card'><h3>2. Choose a Feature</h3></div>", unsafe_allow_html=True)
    
    # Redesigned Feature Selection
    st.markdown("""
    <style>
        .radio-label {
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }
        .description {
            font-size: 14px;
            color: #555;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    feature = st.radio(
        "Select one of the following features:",
        options=["🔍 Describe Scene", "📝 Extract Text", "🔊 Text-to-Speech"],
        format_func=lambda x: x.split(" ")[1]  # Simplifies label formatting
    )
    
    if feature == "🔍 Describe Scene":
        st.markdown("<p class='description'>This feature analyzes the image and provides a detailed scene description for better understanding.</p>", unsafe_allow_html=True)
    elif feature == "📝 Extract Text":
        st.markdown("<p class='description'>This feature uses OCR to extract text from the image, enabling reading of signs, documents, or other text.</p>", unsafe_allow_html=True)
    elif feature == "🔊 Text-to-Speech":
        st.markdown("<p class='description'>This feature converts the extracted text from the image into speech for an auditory experience.</p>", unsafe_allow_html=True)

    # Processing Based on Selected Feature
    input_prompt = """
    Describe the scene in detail, listing key objects, their purpose, and helpful actions for the visually impaired.
    """
    image_data = prepare_image_data(uploaded_file)

    if feature == "🔍 Describe Scene":
        with st.spinner("Generating description..."):
            description = generate_scene_description(input_prompt, image_data)
            st.markdown("<div class='card'><h3>Scene Description</h3></div>", unsafe_allow_html=True)
            st.write(description)

    elif feature == "📝 Extract Text":
        with st.spinner("Extracting text..."):
            extracted_text = extract_text_from_image(image)
            st.markdown("<div class='card'><h3>Extracted Text</h3></div>", unsafe_allow_html=True)
            st.text_area("Extracted Text", extracted_text, height=150)

    elif feature == "🔊 Text-to-Speech":
        with st.spinner("Converting text to speech..."):
            extracted_text = extract_text_from_image(image)
            if extracted_text.strip():
                audio_path = text_to_speech(extracted_text)
                st.success("Audio generated successfully!")
                st.audio(audio_path, format="audio/mp3")
            else:
                st.warning("No text found to convert.")
