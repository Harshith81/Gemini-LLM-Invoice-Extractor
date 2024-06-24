# Q&A Chatbot
#from langchain.llms import OpenAI

# import and load env libraries
from dotenv import load_dotenv
load_dotenv()  
# take environment variables from .env.
import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image

import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get respones

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt]) 
    # it will be in a list format so we need to convert it into string
    return response.text
    

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

st.set_page_config(page_title="Gemini Image Extractor :)")

st.header("Gemini LLM Multi-Language Invoice Extractor")
input=st.text_input("Type your Query & Press Enter : ",key="input")
uploaded_file = st.file_uploader("Click Browse Files to choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)


submit=st.button("Get Response")

input_prompt = """
               You are an expert in understanding invoices, marksheets, prescriptions, charts, notes, and payment receipts.
               You will receive the input query and invoices in the form of input images &
               you will have to answer questions based on the input image and query where you need to scan the entire image and cross check the responces because the input images will be consisting of multiple languages and you need to provide the responce in english and you need to give the responce in a clear, concise and detail format without any mistakes, errors and missing of data.
               At the end of response say Thank you.
               """

## If ask button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("Extracted Details: ")
    st.write(response)



