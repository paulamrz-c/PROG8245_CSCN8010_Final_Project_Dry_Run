# Student Self-Service Chatbot: Proof of Concept

This repository presents a **Proof of Concept (PoC)** for a chatbot designed to reduce the workload of Student Success Advisors by answering frequent student queries using **NLP**, **semantic search**, and **predictive classification**.

## Project Structure

Student Self-Service Chatbot/

├── data/

│   ├── raw/                   # Original input data (PDFs, CSV)

│   └── processed/             # Cleaned CSVs and vector pickles

├── models/                   # Trained classifier, Label Encoder  

├── notebooks/                # Jupyter notebooks for end-to-end pipeline for building the chatbot's backend.

│   ├── 01_scrapping.ipynb

│   ├── 02_extract_FAQs_Resources.ipynb

│   ├── 03_build_embeddings.ipynb

│   └── 04_train_classifier.ipynb

├── resources/                # Architecture diagrams and submission instructions

├── src/                      # All backend source code

│   ├── api.py                # FastAPI app for query prediction

│   ├── chatbot_interface.py  # Streamlit frontend

│   ├── retriever.py          # Embedding search, classifier + LLM fallback

│   ├── query_classifier.py   # PyTorch classifier for query type

│   ├── embedding_hf.py       # SentenceTransformer encoder

│   ├── models.py             # Classifier architecture (torch.nn)

│   ├── openai_utils.py       # (Optional) support for OpenAI APIs

│   └── test.py               # Unit testing logic

├── docs/                     # GitHub Pages static site

│   ├── index.html            # HTML report for project presentation

├── requirements.txt          # Python dependencies

└── README.md                 # Project overview

## NLP Pipeline

-  Text normalization: `ftfy`, `unicodedata`, `re` (used only for Word2Vec and GloVe)
-  Lemmatization & tokenization: `spaCy` (only used for Word2Vec and GloVe)
-  Vectorization: 
    - Word2Vec: Trained on local FAQs and student resources
    - GloVe: Pretrained (100d) from Stanford
    - HuggingFace Sentence Transformers: all-MiniLM-L6-v2 – used as final model due to superior semantic precision
-  Query classification: `faq`, `resource`, `chitchat`, `offramp` (using PyTorch model)

## Corpus Construction

- Extracted FAQs from Winter 2024 PDF documents
- Scraped resources from Conestoga's [Student Success Portal](https://successportal.conestogac.on.ca/)
- Combined into a unified document base with associated embeddings


##  Retrieval Logic (Retriever)

**This is the brain of the chatbot system, implemented in src/retriever.py:**

Receives a student query and classifies it as faq, resource, chitchat, or offramp
Encodes the query into a vector using the selected embedding model (Word2Vec, GloVe, or HuggingFace)
Compares the query vector with all document vectors using cosine similarity
If the similarity is high (> 0.8), returns the matched FAQ or resource directly (even for chitchat)
If similarity is too low or if the query is chitchat/offramp, falls back to an LLM response or human advisor escalation

- Receives a student query and classifies it as faq, resource, chitchat, or offramp
- Encodes the query into a vector using the selected embedding model (Word2Vec, GloVe, or HuggingFace)
- Compares the query vector with all document vectors using cosine similarity
- If the similarity is high (> 0.8), returns the matched FAQ or resource directly (even for `chitchat`)
- Otherwise, if similarity is too low or if the query is chitchat/offramp, fall back to a generative model (`distilgpt2`) or escalate to human advisor


##  Demo Features
Ask natural language questions like:
"Where can I upload my ONE Card photo?"
"Where can I find my timetable?"
"What is VMock?"
"How can I pay my fees"

### Answers are returned with:
💬 Relevant info (answer or link)
📄 Source (FAQ or resource)
📈 Similarity score
🔁 Escalation fallback via LLM (if needed)

## Models Used
- Word2Vec: Trained on internal FAQs + resources
- GloVe: Pre-trained 100d vectors from Stanford NLP
- HuggingFace: all-MiniLM-L6-v2 for contextual sentence embeddings
- DistilGPT2: Used as LLM fallback for chitchat and low similarity

## To Do
- Override chitchat if semantic similarity is very high
- Feedback loop: Let users flag incorrect answers
- Deploy to Streamlit Cloud / Render

## Authors
- Paula Ramirez (8963215)
- Babandeep (9001552)
- Hasyashri Bhatt (9028501)


##  **How to Run the Application**

### 1. Activate your virtual environment (PowerShell):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\activate
```
### 2. Run the FastAPI backend:
```powershell
streamlit run src/chatbot_interface.py --server.port 8501
```
### 3. Launch the Streamlit chatbot interface:
```powershell
streamlit run src/chatbot_interface.py --server.port 8501
```

