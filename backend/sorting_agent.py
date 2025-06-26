from sentence_transformers import SentenceTransformer
from .question_types import ConceptualUnderstanding, ProblemSolving, AppliedGuidance
from sentence_transformers import util

"""Implementing an agent to agent protocol, this model will sort the 
question from the user into one of three categories, to get a deterministic 
response from Gemini. This will be implemented by encoding the question
and using cosine similarity. """



model = SentenceTransformer("all-MiniLM-L6-v2")

question_types = {
    "ConceptualUnderstanding": "Explain a concept in simple terms.",
    "ProblemSolving": "Help solve a technical or coding problem.",
    "AppliedGuidance": "Give advice on how to use or apply a concept in a project."    
}


def classify_question(question: str) -> str: 
    question_embedding = model.encode(question, convert_to_tensor=True)
    type_embeddings = model.encode(list(question_types.values()), convert_to_tensor=True)
    
    similarities = util.cos_sim(question_embedding, type_embeddings)
    best_idx = similarities.argmax().item()
    return list(question_types.keys())[best_idx]
    
    
    
    




