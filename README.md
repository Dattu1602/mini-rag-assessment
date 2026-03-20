# Construction AI Assistant (Mini RAG)

A Retrieval-Augmented Generation (RAG) chatbot designed to answer questions using internal construction documents.

## Architecture
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Store**: FAISS (local index)
- **LLM**: OpenRouter API (`mistralai/mistral-7b-instruct:free` or similar) with fallback to local open-source Ollama (`llama3.2`).
- **Backend / API**: FastAPI + LangChain
- **Frontend**: Custom HTML/CSS/Vanilla JS interface.

## Quickstart

### 1. Prerequisites
- Python 3.10+
- (Optional) OpenRouter API key.

### 2. Environment Setup
```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install requirements
pip install -r backend/requirements.txt
```

### 3. Configure LLM
Copy `.env.example` to `.env` and optionally define `OPENROUTER_API_KEY=...`. If empty, the app will try connecting to a local Ollama service.

### 4. Build the Knowledge Base
Process the provided markup documents and build the FAISS index:
```powershell
python backend/document_processor.py
```

### 5. Start the Server (Local)
Run the FastAPI backend:
```powershell
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
Open your browser to `http://localhost:8000` to interact with the chatbot frontend.

---

## Deployment Options

### Option 1: Render (Easiest)
1. **GitHub Sync**: Connect your repository.
2. **Build Command**: `pip install -r backend/requirements.txt && python backend/document_processor.py`
3. **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

### Option 2: Railway or Fly.io (Docker)
The repository includes a `Dockerfile`. These platforms will automatically detect it:
1. **GitHub Sync**: Point it to this repo.
2. **Automatic Build**: The platform will build the container and serve it on port 8000.

### Option 3: Hugging Face Spaces (AI Optimized)
1. Create a "Docker" Space on Hugging Face.
2. Connect this GitHub repository.
3. It will host the model and frontend with high availability.

---

## Evaluation & Quality Analysis (Bonus)

To evaluate groundedness and accuracy, here are 10 test questions derived *strictly* from the provided Indecimal construction documents:

1. What is the per square foot price for the Premier package?
2. How many critical checkpoints are covered in the quality assurance system?
3. What brands of cement are used in the Infinia package?
4. How does the Escrow-based payment model protect customers?
5. What is the wallet allowance for a main teak door in the Pinnacle package?
6. Which package includes Asian Paints Royale Emulsion for interior painting?
7. What is the standard floor-to-floor ceiling height across all packages?
8. What mechanisms are used to enforce the Zero-Tolerance Policy on construction delays?
9. Does the company provide post-handover maintenance support?
10. What is the maximum wallet allowance for a sink in the Essential package?

### Observations:
- **Grounding Validation**: The model rigorously follows its strict prompt directives. If asked outside knowledge (e.g. *"how should weather delay be documented?"*), it correctly defaults to answering: *"I don't know based on the provided documents"* rather than hallucinating an answer!
- **Transparency**: Every answer generated through the UI explicitly lists the retrieved chunks and source filenames used for formulation.
- **Speed**: The local FAISS/TF-IDF semantic search avoids round-trip latency, enabling instant context injection for the local LLM.


### Appendix: Automated QA Test Runs

**Q1: What is the per square foot price for the Premier package?**

> **A:** ₹1,995 /sqft (incl. GST).

*Sources Retrieved: 4 chunks*

---

**Q2: How does the Escrow-based payment model protect customers?**

> **A:** According to doc3.md, Customer payments are made to an escrow account. A project manager verifies stage completion, and funds are disbursed to the construction partner after verification, which makes contractor payments "stage-based". This ensures that payments are released only after verified completion, reducing financial risk for customers and improving transparency and trust.

*Sources Retrieved: 4 chunks*

---


### Appendix: Automated QA Test Runs & Results

Below are the transcriptions of automated testing queries run directly against the local RAG pipeline to evaluate grounding, completeness, and hallucination prevention.

**Q1: What is the per square foot price for the Premier package?**

> **A:** ₹1,995 /sqft (incl. GST).

*Sources Retrieved: 4 chunks*

---

**Q2: How many critical checkpoints are covered in the quality assurance system?**

> **A:** According to doc3.md, the Quality Assurance System covers 445+ critical checkpoints.

*Sources Retrieved: 4 chunks*

---

**Q3: What brands of cement are used in the Infinia package?**

> **A:** JSW or Jindal Panther.

*Sources Retrieved: 4 chunks*

---

**Q4: How does the Escrow-based payment model protect customers?**

> **A:** The flow emphasizes receiving plans that include detailed design and cost plans with transparent pricing and “no hidden surprises.”

*Sources Retrieved: 4 chunks*

---

**Q5: What is the wallet allowance for a main teak door in the Pinnacle package?**

> **A:** The wallet allowance for a main teak door in the Pinnacle package is ₹50,000.

*Sources Retrieved: 4 chunks*

---

**Q6: Which package includes Asian Paints Royale Emulsion for interior painting?**

> **A:** I don't know based on the provided documents. The document does not mention which package includes Asian Paints Royale Emulsion for interior painting, only that Pinnacle is equivalent to Asian Paints Royale Emulsion for exterior painting.

*Sources Retrieved: 4 chunks*

---

**Q7: What is the standard floor-to-floor ceiling height across all packages?**

> **A:** The standard floor-to-floor height across all packages is 10 ft.

*Sources Retrieved: 2 chunks*

---

**Q8: What mechanisms are used to enforce the Zero-Tolerance Policy on construction delays?**

> **A:** Indecimal uses an integrated project management system, daily tracking of projects, instant flagging of deviations, automated task assignment, and penalisation to reinforce accountability.

*Sources Retrieved: 4 chunks*

---

**Q9: Does the company provide post-handover maintenance support?**

> **A:** Yes, Indecimal provides post-handover maintenance support as part of their long-term care positioning. (Source: doc1.md, Section 10 "Maintenance")

*Sources Retrieved: 4 chunks*

---

**Q10: What is the maximum wallet allowance for a sink in the Essential package?**

> **A:** According to doc2.md, the maximum wallet allowance for a sink in the Essential package is up to ₹4,000 (single bowl).

*Sources Retrieved: 4 chunks*

---

**Q11: What factors affect construction project delays?**

> **A:** Based on the provided documents, the following factors can affect construction project delays:

1. Integrated project management system
2. Daily tracking of projects
3. Instant flagging of deviations
4. Automated task assignment
5. Penalties for delays (as part of the zero-tolerance policy)

These operational mechanisms are designed to minimize delays and ensure on-time delivery, reducing financial risk for customers and improving transparency and trust.

*Sources Retrieved: 4 chunks*

---

**Q12: How should weather delays be documented?**

> **A:** I don't know based on the provided documents. The context does not mention how weather delays should be documented.

*Sources Retrieved: 3 chunks*

---

**Q3: How should weather delays be documented?**

> **A:** I don't know based on the provided documents. The context mentions that Indecimal has a zero-tolerance policy on construction delays, but it does not specify how weather delays should be documented.

*Sources Retrieved: 3 chunks*

---

