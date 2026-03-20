import os
import glob
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

def simple_chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = start + chunk_size
        if end < text_len:
            last_newline = text.rfind('\n', start, end)
            last_period = text.rfind('. ', start, end)
            break_point = max(last_newline, last_period + 1 if last_period != -1 else -1)
            if break_point != -1 and break_point > start + chunk_size // 2:
                end = break_point
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
    return chunks

def process_documents():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    vectorstore_path = os.path.join(base_dir, "vectorstore.pkl")

    print(f"Loading documents from {data_dir}...")
    documents = [] # list of dicts
    
    for filepath in glob.glob(os.path.join(data_dir, "*.md")):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                filename = os.path.basename(filepath)
                documents.append({"content": content, "source": filename})
                print(f"Loaded: {filename}")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    if not documents:
        print("No documents found in the data directory!")
        return

    print("Splitting documents into chunks...")
    chunks = []
    for doc in documents:
        doc_chunks = simple_chunk_text(doc["content"], 500, 50)
        for c in doc_chunks:
            chunks.append({"page_content": c, "metadata": {"source": doc["source"]}})
            
    print(f"Created {len(chunks)} chunks.")

    print("Generating TF-IDF embeddings and building index...")
    texts = [c["page_content"] for c in chunks]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)

    index_data = {
        "vectorizer": vectorizer,
        "tfidf_matrix": tfidf_matrix,
        "chunks": chunks
    }

    print(f"Saving vector index to {vectorstore_path}...")
    with open(vectorstore_path, 'wb') as f:
        pickle.dump(index_data, f)
    print("Vector index created and saved successfully.")

if __name__ == "__main__":
    process_documents()
