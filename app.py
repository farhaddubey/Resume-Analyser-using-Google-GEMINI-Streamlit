# 1. Field to put my Job Description
# 2. Uploading PDF
# 3. PDF to image conversion ---->processing---->Google Gemini Pro
# 4. Prompts Template(Multiple)
import os

import streamlit as st
from dotnev import load_dotenv

load_dotenv()
import google.generativeai as genai
import pdf2image
from PIL import Image

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.txt

def input_pdf_setup(upload_file):
    if upload_file is not None:
        # Converting the pdf to image 
        images = pdf2image.convert_from_bytes(upload_file.read())
        first_page=images[0]

        # Converting to bytes 
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit app

st.set_page_config(page_title='ATS Resume Export')
st.header('ATS Tracking System')
input_text = st.text_area("Job Description", key="input")
uploaded_file=st.file_uploader("Uploader your resume(PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about the resume")
submit2 = st.button("How can I improve my skills?")
submit3 = st.button("Percentage match")

input_prompt1 ="""
You are an experienced Technical Human Resource Manager, experienced in the filled of Data Science, full stack web development, your task is to review the provided resume. Please share your professional evaluation on whether the candidate's profile aligns with Highlight the strengths and weaknesses ot the applicant in relation to the specified job description."""
input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
    
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")


