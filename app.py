import os
from dotenv import load_dotenv
from PIL import Image
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Gemini API
api_key = os.getenv("GOOGLE_API")
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

genai.configure(api_key=os.getenv("GOOGLE_API"))
model = genai.GenerativeModel('gemini-1.5-flash')  # You can use 'gemini-2.0' only if it's available in your region

# Streamlit UI
st.header(':blue[Minutes of Meeting (MoM) Generator]', divider=True)
st.subheader('Upload your handwritten MoM image')

uploaded_file = st.file_uploader('Upload Image', type=['jpg', 'jpeg', 'png'])

# Prompt for Gemini
prompt = '''You are an intelligent assistant tasked with generating structured Minutes of Meeting (MoM) based on handwritten notes and to-dos provided as images. 
Your job is to extract text from the images and organize the information into a clean, professional table with the following columns:
| Particulars (To-Dos) | Deadline | Status (Completed / Pending / Not Started) | % Completion |

Requirements:
- OCR: Accurately read and transcribe handwritten text from the uploaded images.
- Task Identification: Identify individual to-do items, action points, or tasks from the transcribed text.
- Deadline Detection: Detect any mentioned dates or inferred deadlines related to each task. If no deadline is present, leave the field blank or mark as “TBD.”
- Status Assignment: Based on context (e.g., checkmarks, strikethroughs, annotations like "done", "in progress", "to-do", etc.), assign a task status:
  ✅ Completed
  🕒 Pending
  ⏳ Not Started
- Completion %: Estimate a percentage completion (e.g., 0%, 50%, 100%) based on the language or markings (e.g., “half done”, “in progress”, “✓✓✓”, etc.).
'''

# Main logic
if uploaded_file is not None:
    try:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_container_width=True)

        with st.spinner('Extracting and analyzing the image...'):
            response = model.generate_content([img, prompt])
            st.success('Extraction Completed')
            st.markdown(response.text)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
else:
    st.info("Please upload an image to proceed.")
