Welcome to my Personal Assistant project!

The goal of this project is to hone my skills and gain more knowledge by
building tools. I will be building a RAG agent with an LLM to help me (and
possibly others) with revising their chaotic notes. 

The tech stack consists of purely Python. The following libraries 
will be used: 

- FastAPI
- LangChain
- Google Vertex AI
- Google Cloud AI Platform
- Sentence Transformers
- FAISS
- dotenv
- streamlit (Frontend)

I chose Google's API for convenience, since I have quite a few GCP credits
and would like to use them. Feel free to rework the code to fit your preferences, 
for example using OpenAI's API, and so on. 

To run this locally, make sure you install all dependencies within requirements.txt
and run this in your terminal while being in the project root:
uvicorn backend.main:app --reload 

Then to run the frontend, navigate to the frontend folder and run: 
streamlit run streamlit_app.py 

Google gives around 300€ in free credits, and have many tutorials on how 
to use their cloud platform: https://cloud.google.com/free/

You can get your own service account key this way
and run the app locally. In the event that I do deploy this, I will have to add
some rate limiter for API usage, but this was mainly made just to gain more knowledge. 

