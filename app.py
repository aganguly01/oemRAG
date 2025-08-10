import json
import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
from transformers import pipeline

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
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# --- Add docs ---
for doc in docs:
    vector = embedder.encode(doc["content"]).tolist()
    collection.add(
        documents=[doc["content"]],
        embeddings=[vector],
        ids=[doc["id"]]
    )

# --- Load LLM pipeline ---
llm = pipeline("text2text-generation", model="google/flan-t5-small")

# --- Streamlit UI ---
st.title("OEM RAG Demo — With and Without LLM")

query = st.text_input("Enter your question:")

use_llm = st.checkbox("Use LLM to generate answer", value=True)

if query:
    # Embed query
    q_vector = embedder.encode(query).tolist()

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
        prompt = f"Answer the question based on the context below:\n\nContext:\n{combined_context}\n\nQuestion: {query}\nAnswer:"
        output = llm(prompt, max_length=200, do_sample=False)[0]['generated_text']
        st.subheader("Generated Answer (LLM)")
        st.write(output)
    else:
        # No LLM: just show combined retrieved context as "answer"
        st.subheader("Answer (No LLM)")
        st.write(combined_context)

