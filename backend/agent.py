from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .sorting_agent import classify_question
from .question_types import ConceptualUnderstanding, ProblemSolving, AppliedGuidance
from vertexai import init
from dotenv import load_dotenv
from typing import List
from pydantic import ValidationError
import json
import os 
import re 


"""Using dotenv for security reasons as this code is publicly available
on Github, and I do not want my API key exposed. As a private user, 
running this code locally or on the cloud for personal use, you can just 
use the relative path for your API key. """

load_dotenv()
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

init(
    project="woven-nimbus-461919-j1",  
    location="us-central1"  
)

model_name = "gemini-2.5-flash"
question_type_to_model = {
    "ConceptualUnderstanding": ConceptualUnderstanding,
    "ProblemSolving": ProblemSolving,
    "AppliedGuidance": AppliedGuidance,
}

# Initialize the model via langchain
instruct_llm = ChatVertexAI(
    model_name=model_name,
    temperature=0.2,
    max_output_tokens=3500
)

prompt_template = ChatPromptTemplate.from_template("""
<Prompt>
  <Role>You are an AI-powered personal tutor built on Gemini 2.5 Flash, designed to support long-term learning for engineering students, including computer science.</Role>
  <UserProfile>
    <Level>University student (undergraduate or master's)</Level>
    <Field>General Engineering (e.g., Electrical, Mechanical, Computer Science, Software Engineering)</Field>
    <LearningGoals>
      <Goal>Develop a strong conceptual foundation</Goal>
      <Goal>Build long-term retention of key topics</Goal>
      <Goal>Gain confidence in solving real-world problems</Goal>
    </LearningGoals>
    <LearningStyle>
      <Style>Step-by-step reasoning</Style>
      <Style>Analogies and examples</Style>
      <Style>Concise explanations with clarity</Style>
      <Style>Prefers accurate citations from retrieved materials</Style>
    </LearningStyle>
    <TechnologyUsed>
      <System>Gemini 2.5 Flash</System>
      <Technique>Retrieval-Augmented Generation (RAG)</Technique>
    </TechnologyUsed>
  </UserProfile>
  <Scope>
    <Term>Long-term educational support across engineering domains</Term>
    <Function>Interactive tutor capable of adapting to evolving student knowledge</Function>
    <ContextualAwareness>Continuously reference and incorporate retrieved documents via RAG</ContextualAwareness>
  </Scope>
  <Instructions>
    <ExplainClearly>Use simple, accurate language</ExplainClearly>
    <BuildUnderstanding>Break down complex ideas into logical steps</BuildUnderstanding>
    <UseAnalogies>When helpful, relate concepts to everyday ideas or relevant engineering fields</UseAnalogies>
    <ReferenceRAG>Always cite or refer precisely to RAG-sourced context if applicable</ReferenceRAG>
    <HandleUnknowns>Admit when information is missing or unavailable</HandleUnknowns>
    <KeepConcise>Be concise, but provide slightly more detail where it supports clarity or deeper understanding</KeepConcise>
    <ExpandWhenHelpful>If the context allows, expand slightly on important distinctions, conceptual reasoning, and practical applications</ExpandWhenHelpful>
    <IncorporateUseCases>If the question expresses confusion about application (e.g., "when to use X vs Y"), include guidance on appropriate use cases</IncorporateUseCases>
    <FinishWithinTokenLimit>Ensure the entire response is complete and fits within the maximum token limit of 2500 tokens.</FinishWithinTokenLimit>
    <OutputFormat>
      Respond ONLY with a valid JSON object matching the appropriate schema based on the question type. DO NOT include explanations or additional text.

      For "ConceptualUnderstanding":
      {{
        "summary": "...",
        "step_by_step_explanation": ["...", "..."],
        "analogy_or_example": "...",
        "key_terms": ["...", "..."],
        "optional_visual_description": "..."
      }}

      For "ProblemSolving":
      {{
        "problem_restatement": "...",
        "assumptions": ["...", "..."],
        "step_by_step_solution": ["...", "..."],
        "final_answer_or_output": "...",
        "common_pitfalls": ["...", "..."],
        "optional_visual_description": "..."
      }}

      For "AppliedGuidance":
      {{
        "goal_or_use_case": "...",
        "prerequisites": ["...", "..."],
        "recommended_approach": "...",
        "actionable_steps": ["...", "..."],
        "timeline_or_phases": ["...", "..."],
        "risks_or_warnings": ["...", "..."],
        "optional_visual_description": "..."
      }}
    </OutputFormat>
  </Instructions>
  <Context>{context}</Context>
  <Question>{question}</Question>
</Prompt>
""")


def generate_answers(query: str, context_chunks: List[str]) -> str: 
    context = " \n".join(chunk["text"] for chunk in context_chunks)
    
    # Identify question type 
    question_type = classify_question(query)
    
    # Chain which will get a clean, generated LLM response
    chain = prompt_template | instruct_llm | StrOutputParser()
    
    prompt_input = {
        "context": context,
        "question": query,
        "question_type": question_type
    }
    
    # Get JSON response as a string
    response_str = chain.invoke(prompt_input).strip()

    # Strip markdown fences if present (just simple cleanup)
    response_str = response_str.strip()
    response_str = re.sub(r"^```(?:json)?\s*", "", response_str)
    response_str = re.sub(r"\s*```$", "", response_str)

    # Assume response_str is valid JSON now, parse directly
    parsed_dict = json.loads(response_str)

    # Convert to Pydantic model (assuming fields are all present and correctly formatted)
    model_class = question_type_to_model.get(question_type)
    structured_output = model_class.model_validate(parsed_dict)
    
    
    return structured_output
    
    
