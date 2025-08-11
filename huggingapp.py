import json
import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from transformers import AutoTokenizer, AutoModel
import torch

# --- Load data ---
with open("incidents.json", "r") as f:
    docs = json.load(f)

# --- Init Chroma client and collection ---
client = chromadb.Client()

collection_name = "incidents_collection"
try:
    client.delete_collection(name=collection_name)
except Exception:
    pass

collection = client.create_collection(name=collection_name)

# --- Load embedder ---
#embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load embedding model (offline)
model_name = "BAAI/bge-small-en-v1.5"
tokenizer = AutoTokenizer.from_pretrained(model_name)
embedding_model = AutoModel.from_pretrained(model_name)

def embed_text(text):
    # Tokenize input
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )
    with torch.no_grad():
        # Mean pooling over the token embeddings
        embeddings = embedding_model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings[0].numpy()


# --- Add docs ---
for doc in docs:
    vector = embed_text(doc["content"]).tolist()
    collection.add(
        documents=[doc["content"]],
        embeddings=[vector],
        ids=[doc["id"]]
    )


# --- Streamlit UI ---
st.title("OEM RAG Demo — With and Without LLM")

query = st.text_input("Enter your question:")

use_llm = st.checkbox("Use LLM to generate answer", value=False)
use_llm = False

if query:
    # Embed query
    #q_vector = embedder.encode(query).tolist()
    q_vector = embed_text(query).tolist()

    # Retrieve top 3 docs from Chroma
    results = collection.query(query_embeddings=[q_vector], n_results=3)

    retrieved_texts = results['documents'][0]
    retrieved_ids = results['ids'][0]

    # Combine retrieved context
    combined_context = "\n\n".join(retrieved_texts)

    st.subheader("Retrieved Context")
    for idx, text in enumerate(retrieved_texts):
        st.markdown(f"**Doc {idx+1} (id: {retrieved_ids[idx]}):** {text}")

    if use_llm:
        # --- Load LLM pipeline ---
        llm = pipeline("text2text-generation", model="google/flan-t5-small")
        prompt = f"Answer the question based on the context below:\n\nContext:\n{combined_context}\n\nQuestion: {query}\nAnswer:"
        output = llm(prompt, max_length=200, do_sample=False)[0]['generated_text']
        st.subheader("Generated Answer (LLM)")
        st.write(output)
    else:
        # No LLM: just show combined retrieved context as "answer"
        st.subheader("Answer (No LLM)")
        st.write(combined_context)

