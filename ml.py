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


def get_openai_api_key():
    os.environ["OPENAI_API_KEY"] = getpass.getpass()


def load_pdf(path):
    loader = PyPDFLoader(path)
    pages = loader.load()
    return pages


def create_vector_store(contents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(contents)
    vector_store = Chroma.from_documents(
        documents=splits, embedding=OpenAIEmbeddings())
    return vector_store


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
