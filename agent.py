from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
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


# Initialize the model via langchain
instruct_llm = ChatVertexAI(
    model_name="gemini-1.5-pro",
    temperature=0.2,
    max_output_token=1024
)

prompt_template = ChatPromptTemplate.from_template("""
You are a helpful note revising assistant. Answer the following question using only the context provided.
If you can't find the answer in the context, say so. Do not just regurgitate information 
or reiterate your thoughts. Help the student understand the topics within the notes. Try to be concise. 

Context: {context}

Question: {question}
""")

def generate_answers(query: str, context_chunks: List[str]) -> str: 
    context = " \n".join(context_chunks)
    
    # Chain which will get a clean, generated LLM response
    chain = prompt_template | instruct_llm | StrOutputParser()
    
    response = chain.invoke({"context": context, "question": query})
    return response 
    
    


