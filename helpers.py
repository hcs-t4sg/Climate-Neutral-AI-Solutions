from secret import OPENAI_API_KEY # You will need to instantiate your own secret.py file
                                  # with the OpenAI key I gave you in the starter project instructions

import time

from langchain.document_loaders import PDFMinerLoader
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter


def initialize_qa_system():
    source_docs_arr = ["nature_based_solutions","climate_change_carbon_intensive_firms"]

    embeddings_list = []

    for source in source_docs_arr:
        loader = PDFMinerLoader(f"source_docs/{source}.pdf")
        pages = loader.load()

        embeddings_instance = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

        # Instantiating Text Splitter
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,  
        chunk_overlap  = 20,
        length_function = len,
        add_start_index = True,
        )

        # Splitting pdf content into text chunks
        texts = text_splitter.split_text(str(pages))

        for text in texts:
            embedding = embeddings_instance.embed_documents([text])[0]  
            embeddings_list.append((text, embedding)) 

    # Use these paired text-embedding tuples to create the FAISS index
    faiss_index = FAISS.from_embeddings(embeddings_list, embeddings_instance)

    llm = OpenAI(openai_api_key=OPENAI_API_KEY)

    # Initialize the QA system with the loaded documents
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=faiss_index.as_retriever())

    return qa

def get_sol(question):
    QA_SYSTEM = initialize_qa_system()
    answer = QA_SYSTEM.run(question)
    return answer




