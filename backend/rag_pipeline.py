import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTORSTORE_PATH = os.path.join(BASE_DIR, "vectorstore.pkl")

def get_llm():
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if openrouter_key:
        print("Using OpenRouter LLM")
        return ChatOpenAI(
            model="meta-llama/llama-3.3-70b-instruct:free",
            openai_api_key=openrouter_key,
            openai_api_base="https://openrouter.ai/api/v1",
            max_tokens=500
        )
    else:
        print("Using local Ollama LLM")
        return ChatOllama(model="llama3.2")

def setup_rag_pipeline():
    if not os.path.exists(VECTORSTORE_PATH):
        print("Warning: Vectorstore not found! Run document_processor.py.")
        return None
    
    with open(VECTORSTORE_PATH, 'rb') as f:
        index_data = pickle.load(f)
        
    vectorizer = index_data["vectorizer"]
    tfidf_matrix = index_data["tfidf_matrix"]
    chunks = index_data["chunks"] # list of dicts

    template = """You are an AI assistant for a construction marketplace.
Your job is to answer user questions STRICTLY based on the provided context document chunks.
If the answer cannot be found in the context, say "I don't know based on the provided documents." Do not attempt to guess, hallucinate, or use outside knowledge.

Context:
{context}

Question: {question}

Answer:"""
    prompt = PromptTemplate.from_template(template)
    llm = get_llm()

    def retrieve(query, k=4):
        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        top_k_indices = similarities.argsort()[-k:][::-1]
        
        docs = []
        for idx in top_k_indices:
            if similarities[idx] > 0.02:
                docs.append(chunks[idx])
        return docs

    def format_docs(docs):
        return "\n\n".join(f"[Source: {doc['metadata'].get('source', 'Unknown')}]\n{doc['page_content']}" for doc in docs)

    def ask_question(question: str):
        docs = retrieve(question)
        if not docs:
            context_str = "No relevant context found."
        else:
            context_str = format_docs(docs)
        
        # List of verified reliable free models to try in case of rate limits (429) or failures
        models_to_try = [
            "nvidia/nemotron-3-super-120b-a12b:free",
            "minimax/minimax-m2.5:free",
            "google/gemini-2.0-flash-lite-preview-02-05:free",
            "meta-llama/llama-3.3-70b-instruct:free"
        ]
        
        last_error = None
        for model_id in models_to_try:
            try:
                # Update LLM model for this attempt
                llm.model_name = model_id
                chain = prompt | llm | StrOutputParser()
                answer = chain.invoke({"context": context_str, "question": question})
                
                return {
                    "answer": answer,
                    "context": [{"source": doc['metadata'].get("source", "Unknown"), "content": doc['page_content']} for doc in docs]
                }
            except Exception as e:
                last_error = str(e)
                print(f"Model {model_id} failed: {last_error}. Trying next...")
                continue
        
        # If all fail, return the last error
        return {
            "answer": f"Error: All available free models are currently rate-limited or unavailable. Please try again in a few minutes. (Last error: {last_error})",
            "context": []
        }

    return ask_question

rag_ask = setup_rag_pipeline()
