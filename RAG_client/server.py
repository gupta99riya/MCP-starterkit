from mcp.server.fastmcp import FastMCP
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter # type: ignore
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq  # Groq LLM
import os
import requests
# https://www.analyticsvidhya.com/blog/2025/06/rag-with-mcp/

# Create an MCP server
mcp = FastMCP("RAG")


# Set up embeddings (You can pick a different Hugging Face model if preferred)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# Set up Groq LLM
model = ChatGroq(
   model_name="llama3-8b-8192",  # or another Groq-supported model
   groq_api_key="" # Required if not set via environment variable
)


# Load documents
loader = TextLoader("dummy.txt")
data = loader.load()


# Document splitting
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(data)


# Vector DB
docsearch = Chroma.from_documents(texts, embeddings)


# Retriever chain
qa = RetrievalQA.from_chain_type(llm=model, retriever=docsearch.as_retriever())


@mcp.tool()
def retrieve(prompt: str) -> str:
   """Get information using RAG"""
   return qa.invoke(prompt)


if __name__ == "__main__":
   mcp.run()