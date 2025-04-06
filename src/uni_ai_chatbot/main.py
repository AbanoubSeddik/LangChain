import os
from pathlib import Path

from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_text_splitters import CharacterTextSplitter

from uni_ai_chatbot.resources import get_resource

# Get Ollama host from environment variable or use default
ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

file_path = get_resource(relative_path=Path("data.txt"))
loader = TextLoader(file_path)
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
split_docs = text_splitter.split_documents(documents)

texts = [doc.page_content for doc in split_docs]

# Use environment-configured Ollama host
embeddings = OllamaEmbeddings(model="llama3.2:latest", base_url=ollama_host)
vector_store = FAISS.from_texts(texts, embeddings)
retriever = vector_store.as_retriever()

# Use environment-configured Ollama host
llm = OllamaLLM(model="llama3.2:latest", base_url=ollama_host)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


def run_queries():
    queries = []

    print("Enter your queries (type 'done' to finish):")
    while True:
        query = input("> ")
        if query.lower() == "done":
            break
        queries.append(query)

    for query in queries:
        print(f"\nQuery: {query}")
        response = qa_chain.invoke(query)
        print(f"Response: {response['result']}")


if __name__ == "__main__":
    run_queries()