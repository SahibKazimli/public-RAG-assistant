import streamlit as st
from dotenv import load_dotenv
import requests
import os

load_dotenv()
BACKEND_URL = "http://localhost:8000"

st.title("Revising Assistant")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file: 
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    req = requests.post(f"{BACKEND_URL}/upload", files=files)
    if req.ok: 
        st.success("File uploaded successfully!")
        
question = st.text_area("Ask a question about your notes", height=150)

def display_conceptual_understanding(data):
    st.header("Summary")
    st.write(data.get("summary", ""))

    st.header("Step-by-step Explanation")
    for step in data.get("step_by_step_explanation", []):
        st.write(f"- {step}")

    st.header("Analogy or Example")
    st.write(data.get("analogy_or_example", ""))

    st.header("Key Terms")
    for term in data.get("key_terms", []):
        st.write(f"- {term}")

    if data.get("optional_visual_description"):
        st.header("Visual Description")
        st.write(data["optional_visual_description"])

def display_problem_solving(data):
    st.header("Problem Restatement")
    st.write(data.get("problem_restatement", ""))

    st.header("Assumptions")
    for a in data.get("assumptions", []):
        st.write(f"- {a}")

    st.header("Step-by-step Solution")
    for step in data.get("step_by_step_solution", []):
        st.write(f"- {step}")

    st.header("Final Answer or Output")
    st.write(data.get("final_answer_or_output", ""))

    st.header("Common Pitfalls")
    for pitfall in data.get("common_pitfalls", []):
        st.write(f"- {pitfall}")

    if data.get("optional_visual_description"):
        st.header("Visual Description")
        st.write(data["optional_visual_description"])

def display_applied_guidance(data):
    st.header("Goal or Use Case")
    st.write(data.get("goal_or_use_case", ""))

    st.header("Prerequisites")
    for pre in data.get("prerequisites", []):
        st.write(f"- {pre}")

    st.header("Recommended Approach")
    st.write(data.get("recommended_approach", ""))

    st.header("Actionable Steps")
    for step in data.get("actionable_steps", []):
        st.write(f"- {step}")

    st.header("Timeline or Phases")
    for phase in data.get("timeline_or_phases", []):
        st.write(f"- {phase}")

    st.header("Risks or Warnings")
    for risk in data.get("risks_or_warnings", []):
        st.write(f"- {risk}")

    if data.get("optional_visual_description"):
        st.header("Visual Description")
        st.write(data["optional_visual_description"])

if st.button("Generate Answer"):
    if question: 
        payload = {"query": question}
        req = requests.post(f"{BACKEND_URL}/generate", json=payload)
        if req.ok: 
            response = req.json()
            # Assume your backend sends back question_type with the response (recommended)
            question_type = response.get("question_type", "ConceptualUnderstanding")  # fallback
            
            # The actual data part from response might differ depending on your backend
            data = response.get("data", response)  # adapt as needed
            
            if question_type == "ConceptualUnderstanding":
                display_conceptual_understanding(data)
            elif question_type == "ProblemSolving":
                display_problem_solving(data)
            elif question_type == "AppliedGuidance":
                display_applied_guidance(data)
            else:
                st.write(data)  # fallback to raw output
        else: 
            st.error("Error getting response")
    else: 
        st.warning("Please enter a question")