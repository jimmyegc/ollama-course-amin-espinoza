import requests
import json
import chromadb

chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection(name="pdf_chunks")

def embed_text(text, model="nomic-embed-text"):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": model, "prompt": text}
    )
    return response.json()["embedding"]

def retrieve(quer, n=3):
    query_embedding = embed_text(quer)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n
    )
    return results["documents"][0]

def ask_llm(question, context, model):
    prompt = f"Usa el contexto siguiente:\n\n{context}\n\nPara responder a la pregunta:\n\n{question}"
    response  = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt}
    )
    answer = ""
    for chunk in response.iter_lines():
        if chunk:
            data=json.loads(chunk.decode())
            answer+=data.get("response","")
        
    return answer

question = input("Pregunta: ")
answer = ask_llm(question, "\n".join(retrieve(question)), model="llama3.2")
print(f"Respuesta: {answer}")   