from secret import OPENAI_API_KEY # You will need to instantiate your own secret.py file
                                  # with the OpenAI key I gave you in the starter project instructions

# # Eventually will become our function that will get the climate-netural solution using LangChain
# # For the starter project, implement your work here!
#def get_sol(query):
#  pass















# from langchain.chains import RetrievalQA
# from langchain.document_loaders import TextLoader
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.llms import OpenAI
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import Chroma

# def initialize_qa_system():
#     # Load documents from source_docs
#     loader = TextLoader("Climate-Neutral-.-Solutions/source_docs/climate_change_carbon_intensive_firms.pdf")
#     documents = loader.load()

#     # Tokenize the documents
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     texts = text_splitter.split_documents(documents)

#     # Create embeddings and doc search
#     embeddings = OpenAIEmbeddings()
#     docsearch = Chroma.from_documents(texts, embeddings)

#     # Initialize the Question Answering system
#     qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())
#     return qa

# QA_SYSTEM = initialize_qa_system()

# def get_sol(query):
#     return QA_SYSTEM.run(query)

import time

from langchain.document_loaders import PDFMinerLoader
# Assuming that there is a RetrievalQA system or similar in langchain
from langchain.chains import RetrievalQA

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

def initialize_qa_system():
    # Load documents from the provided PDF
    loader = PDFMinerLoader("source_docs/nature-based-solutions.pdf")

    pages = loader.load()

    time.sleep(20)  # Introducing a 20 seconds timeout

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    time.sleep(20)  # Introducing a 20 seconds timeout
    
    faiss_index = FAISS.from_documents(pages, embeddings)
    
    llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    time.sleep(20)  # Introducing a 20 seconds timeout

    # Initialize the QA system with the loaded documents
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=faiss_index.as_retriever())
    
    return qa


def get_sol(question):
    QA_SYSTEM = initialize_qa_system()

    # Query the QA system for an answer
    answer = QA_SYSTEM.get_answer(question)
    return answer