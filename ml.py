import os

from langchain_community.document_loaders import PyPDFLoader
import bs4
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)


def get_openai_api_key():
    return os.environ["OPENAI_API_KEY"]


def load_pdf(path):
    loader = PyPDFLoader(path)
    pages = loader.load()
    return pages


# for pdfs only
def create_or_get_vector_store(collection_name, file_path):
    embedding_function = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2")
    langchain_chroma = Chroma(
        persist_directory="dbs", collection_name=collection_name, embedding_function=embedding_function)
    if file_path:
        contents = load_pdf(file_path)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(contents)
        vector_store = Chroma.from_documents(
            documents=splits, embedding=embedding_function, collection_name=collection_name, persist_directory="dbs")
        return vector_store
    return langchain_chroma.get_collection(name=collection_name)


def simple_query(chroma_client, collection_name, query):
    embedding_function = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2")
    embeddings = embedding_function.embed_query(query)
    return chroma_client.get_collection(name=collection_name).query(query_embeddings=[embeddings], n_results=2)


def handle_question(collection_name, question_text):
    embedding_function = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2")
    langchain_chroma = Chroma(
        persist_directory="dbs", collection_name=collection_name, embedding_function=embedding_function)
    retriever = langchain_chroma.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain.invoke(question_text)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
