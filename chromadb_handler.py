import chromadb
from chromadb.utils import embedding_functions
from dummy_documents import documents

import os
import gc
from chromadb.config import Settings

from utils import print_memory_usage

# Define the DB path (works on Render)
chroma_path = os.path.join(os.getcwd(), "rag_db")

client = chromadb.PersistentClient(
    path=chroma_path,
    settings=Settings(allow_reset=True, anonymized_telemetry=False)  # Allows overwriting
)


filtered_documents = [doc for doc in documents if 10 < len(doc) < 200]

print_memory_usage()  # Check memory usage
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

print_memory_usage() 
# Check if the collection exists, otherwise create it
collection_name = "business_knowledge2"
if collection_name in [col.name for col in client.list_collections()]:
    collection = client.get_collection(name=collection_name)
else:
    collection = client.create_collection(
        name=collection_name,
        embedding_function=sentence_transformer_ef
    )

    # Add documents to the DB (assign unique IDs)
    collection.add(
        documents=filtered_documents,
        ids=[f"id{i}" for i in range(len(filtered_documents))]
    )

print_memory_usage() 

gc.collect()
print_memory_usage()  # Check if

def retrieve_context(query: str, top_k: int = 3):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return results["documents"][0]  # Returns top matches

# Example usage
user_query = "What is your return policy?"
context = retrieve_context(user_query)
print_memory_usage()  # Check if
print(context)  # Output: ["Our return policy allows refunds within 30 days."]