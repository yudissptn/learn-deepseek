import chromadb
from chromadb.utils import embedding_functions
from dummy_documents import documents

import os
from chromadb.config import Settings

# Define the DB path (works on Render)
chroma_path = os.path.join(os.getcwd(), "rag_db")

client = chromadb.PersistentClient(
    path=chroma_path,
    settings=Settings(allow_reset=True)  # Allows overwriting
)

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

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
        documents=documents,
        ids=[f"id{i}" for i in range(len(documents))]
    )

def retrieve_context(query: str, top_k: int = 3):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return results["documents"][0]  # Returns top matches

# Example usage
user_query = "What is your return policy?"
context = retrieve_context(user_query)
print(context)  # Output: ["Our return policy allows refunds within 30 days."]