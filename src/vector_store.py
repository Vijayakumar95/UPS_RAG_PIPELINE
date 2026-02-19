import chromadb
import ollama
from chromadb.config import Settings
from config import EMBED_MODEL,CHROMA_DIR,COLLECTION_NAME

client =  chromadb.Client(Settings(persist_directory=CHROMA_DIR))
collection = client.get_or_create_collection(name = COLLECTION_NAME)

def embed_text(text):
    response = ollama.embeddings(model= EMBED_MODEL,prompt = text)
    return response["embedding"]

def clear_collection():
    client.delete_collection(COLLECTION_NAME)
    


def add_documents(chunks):
    print("COLLECTION COUNT BEFORE DELETING-------------")
    # print(collection.count())
    # clear_collection()
    print("CREATING COLLECTION AFTER DELETING---------------")
    client =  chromadb.Client(Settings(persist_directory=CHROMA_DIR))
    collection = client.get_or_create_collection(name = COLLECTION_NAME)
    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        collection.add(ids =[str(i)],embeddings=[embedding],documents=[chunk])
    print(collection.count())

def query_documents(query, top_k=4):
    query_embedding = embed_text(query)
    print("QUERYING COLLECTION---------------")
    results = collection.query(query_embeddings=[query_embedding],n_results=top_k)
    print(results)
    return results["documents"][0]