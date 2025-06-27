<h1>Welcome to my Personal Assistant project!</h1>

This project is a hands-on tool designed to help with revising messy notes using Retrieval-Augmented Generation (RAG) powered by a Large Language Model (LLM).

The goal is to sharpen my skills by building useful tools and experimenting with agent-based design patterns, including agent-to-agent communication.

<h2>What It Does</h2>

- Upload a PDF of notes (even chaotic ones)
- Automatically chunk, embed, and store them in a vector index
- Ask questions about your notes — the assistant will retrieve relevant chunks and generate clear, helpful answers
- Categorizes questions via a sorting agent to route them more effectively (e.g., concept explanations, definitions, workflows)
 

<h2>Tech Stack </h2>

- FastAPI
- LangChain – Agent + Chaining logic
- Google Vertex AI – LLM and embeddings (using gemini-2.5-flash and text-embedding-004)
- Google Cloud AI Platform
- FAISS – Vector Similarity Search
- dotenv – Environment Variable Handling
- Streamlit – Frontend UI

<h3>Running Locally:</h3>
pip install -r requirements.txt

<h3>Start the backend (assuming you are running from the project root):</h3>
uvicorn backend.main:app --reload

<h3>Start the frontend:</h3>
cd frontend
streamlit run streamlit_app.py

<h3>Google Cloud Setup:</h3>
Google offers around €300 in free credits for new users:
https://cloud.google.com/free


</h3>To run this app:</h3>
- Enable Vertex AI and Cloud Storage APIs
- Create a service account and download the JSON key
- Set the following environment variable: GOOGLE_APPLICATION_CREDENTIALS="path/to/your/key.json"


<h3>Future Improvements</h3>
- Add rate limiting if deployed publicly
- Add support for handwritten notes via OCR and/or images
- Improve agent responses with longer context windows or visual reasoning
- Add multiple agents, researcher, rephraser, summarizer for even better output (the project already has a routing agent!)


<h3>Final Notes</h3>
This app is built primarily to learn, explore, and experiment.
Feel free to clone, modify, or use it as a base for your own assistant projects!
Performance was not the focus, but optimally the computationally intensive functions should be written in a high performance language like C++ or Golang.



<img width="1470" alt="Screenshot 2025-06-27 at 00 30 45" src="https://github.com/user-attachments/assets/3a541401-e74e-4e31-af48-69b8e15ef4c6" />

