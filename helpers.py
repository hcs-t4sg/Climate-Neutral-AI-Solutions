from secret import OPENAI_API_KEY # You will need to instantiate your own secret.py file
                                  # with the OpenAI key I gave you in the starter project instructions
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

# PDF reader
from langchain.document_loaders import PyPDFLoader

# Eventually will become our function that will get the climate-netural solution using LangChain
# For the starter project, implement your work here!

def get_sol(query):
  loader = PyPDFLoader("srcdocs/google.pdf")
  documents = loader.load()
  text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
  texts = text_splitter.split_documents(documents)

  embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
  docsearch = Chroma.from_documents(texts, embeddings)

  qa = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=OPENAI_API_KEY), chain_type="stuff", retriever=docsearch.as_retriever(), verbose="True")

  return qa.run(query)