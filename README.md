<h1>Welcome to my Personal Assistant project!</h1>

This project is a hands-on tool designed to help with revising messy notes using Retrieval-Augmented Generation (RAG) powered by a Large Language Model (LLM).

The goal is to sharpen my skills by building useful tools and experimenting with agent-based design patterns, including agent-to-agent communication.

What It Does
- Upload a PDF of notes (even chaotic ones)
- Automatically chunk, embed, and store them in a vector index
- Ask questions about your notes — the assistant will retrieve relevant chunks and generate clear, helpful answers
- Categorizes questions via a sorting agent to route them more effectively (e.g., concept explanations, definitions, workflows)
 

Tech Stack 
- FastAPI
- LangChain – Agent + Chaining logic
- Google Vertex AI – LLM and embeddings (using gemini-2.5-flash and text-embedding-004)
- Google Cloud AI Platform
- FAISS – Vector Similarity Search
- dotenv – Environment Variable Handling
- Streamlit – Frontend UI

Running Locally:
pip install -r requirements.txt

Start the backend (assuming you are running from the project root):
uvicorn backend.main:app --reload

Start the frontend:
cd frontend
streamlit run streamlit_app.py

Google Cloud Setup:
Google offers around €300 in free credits for new users:
https://cloud.google.com/free


To run this app:
- Enable Vertex AI and Cloud Storage APIs
- Create a service account and download the JSON key
- Set the following environment variable: GOOGLE_APPLICATION_CREDENTIALS="path/to/your/key.json"


Future Improvements
- Add rate limiting if deployed publicly
- Add support for handwritten notes via OCR and/or images
- Improve agent responses with longer context windows or visual reasoning
- Add multiple agents, researcher, rephraser, summarizer for even better output (the project already has a routing agent!)


Final Notes
This app is built primarily to learn, explore, and experiment.
Feel free to clone, modify, or use it as a base for your own assistant projects!
Performance was not the focus, but optimally the computationally intensive functions should be written in a high performance language like C++ or Golang.



<img width="1470" alt="Screenshot 2025-06-27 at 00 30 45" src="https://github.com/user-attachments/assets/3a541401-e74e-4e31-af48-69b8e15ef4c6" />

