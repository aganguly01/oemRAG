import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

# -----------------------
# Setup Chroma & TF-IDF
# -----------------------
collection_name = "incidents_collection"
client = chromadb.Client()

# Delete existing collection if any
try:
    client.delete_collection(name=collection_name)
except Exception:
    pass

collection = client.create_collection(name=collection_name)

# Your docs
with open("incidents.json", "r") as f:
    docs = json.load(f)

# Fit TF-IDF
corpus = [doc["content"] for doc in docs]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

# Function to get TF-IDF embedding
def embed_text(text):
    return vectorizer.transform([text]).toarray()[0]

# Add docs to Chroma with TF-IDF vectors
for doc in docs:
    vector = embed_text(doc["content"])
    collection.add(
        documents=[doc["content"]],
        embeddings=[vector.tolist()],
        ids=[doc["id"]]
    )

# -----------------------
# Streamlit UI
# -----------------------
st.title("OEM RAG lookup using sklearn embedding (No LLM)")
query = st.text_input("Enter your query:")
use_llm = st.checkbox("Use LLM to generate answer", value=False)
use_llm = False

if query:
    q_vector = embed_text(query).reshape(1, -1)

    # Retrieve top matches via Chroma
    results = collection.query(
        query_embeddings=q_vector.tolist(),
        n_results=3
    )

    st.subheader("Top Matching Contexts")
    for doc in results["documents"][0]:
        st.write(f"- {doc}")

    # If no LLM, return the top doc as answer
    st.subheader("Answer (No LLM)")
    if results["documents"]:
        st.write(results["documents"][0][0])
