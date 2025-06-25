from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from vertexai import init
from dotenv import load_dotenv
from typing import List
import os 


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

# Initialize the model via langchain
instruct_llm = ChatVertexAI(
    model_name=model_name,
    temperature=0.2,
    max_output_tokens=1800
)

prompt_template = ChatPromptTemplate.from_template("""
You are a friendly and patient study assistant helping a student revise their notes. 
Use only the context provided to answer the question.

- Explain concepts clearly and in simple terms.
- Use examples or analogies where possible.
- Break down complex ideas step-by-step.
- If the answer is not found in the context, say honestly that you don't know.
- Avoid repeating the question or adding unrelated information.
- Help the student truly understand the material.

Keep your answer concise but complete within the token limit.
If the full answer is too long, summarize the key points clearly.

Context: {context}

Question: {question}
""")


def generate_answers(query: str, context_chunks: List[str]) -> str: 
    context = " \n".join(chunk["text"] for chunk in context_chunks)
    
    # Chain which will get a clean, generated LLM response
    chain = prompt_template | instruct_llm | StrOutputParser()
    
    response = chain.invoke({"context": context, "question": query})
    return response 
    
    


