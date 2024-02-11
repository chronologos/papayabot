from flask import Flask, request, jsonify
import os
import logging
import chromadb
import time

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

import getpass
import os

app = Flask(__name__)

def get_openai_api_key():
    os.environ["OPENAI_API_KEY"] = getpass.getpass()

def load_pdf(path):
    loader = PyPDFLoader(path)
    pages = loader.load()
    return pages

def create_vector_store(contents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(contents)
    vector_store = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    return vector_store

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # get API key
    os.environ["OPENAI_API_KEY"] = getpass.getpass()

    # load doc
    file_path = 'MLYearning_AndrewNg.pdf' #request.form['file_path']
    contents = load_pdf(file_path)

    # store embeddings of the doc in a vector store
    vector_store = create_vector_store(contents)

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vector_store.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
    )   

    print (rag_chain.invoke("what is the difference between dev and test set?"))