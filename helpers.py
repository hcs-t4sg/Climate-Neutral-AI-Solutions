from secret import OPENAI_API_KEY # You will need to instantiate your own secret.py file
                                  # with the OpenAI key I gave you in the starter project instructions
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader
#import magic
import os
import nltk

# Eventually will become our function that will get the climate-netural solution using LangChain
# For the starter project, implement your work here!
def get_sol(query):
  loader = PyPDFLoader("source_docs/Corporate_Solutions1.pdf")
  pages = loader.load_and_split()
  text_splitter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
  texts = text_splitter.split_documents(pages)
  embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
  docsearch = Chroma.from_documents(texts, embeddings)
  qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch, verbose=True)

  query = "How should companies cut land-based emissions in their value chain?"
  qa.run(query)


get_sol("a")