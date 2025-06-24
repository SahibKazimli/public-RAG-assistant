import streamlit as st
from dotenv import load_dotenv
import requests
import os

# Replace with your own URL. 
load_dotenv()
BACKEND_URL = "http://localhost:8000"


st.title("Revising Assistant")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file: 
    # Prepare the files dict for requests
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    req = requests.post(f"{BACKEND_URL}/upload", files=files)
    if req.ok: 
        st.success("File uploaded successfully!")
        
    
question = st.text_input("Ask a question about your notes")

if st.button("Generate Answer"):
    if question: 
        payload = {"query":question}
        req = requests.post(f"{BACKEND_URL}/generate", json=payload)
        if req.ok: 
            st.write(req.json())
        else: 
            st.error("Error getting response")
    else: 
        print("Please enter a question")