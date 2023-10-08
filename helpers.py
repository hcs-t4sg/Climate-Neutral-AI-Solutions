from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain import PromptTemplate
import os

# Eventually will become our function that will get the climate-netural solution using LangChain
# For the starter project, implement your work here!
def get_sol(query_params):
  # loader = TextLoader("../../state_of_the_union.txt")
  # documents = loader.load()

  llm = OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])

  loader = PyPDFLoader("source_docs/Meta-2023-Path-to-Net-Zero.pdf")

  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 20,
    length_function = len,
    is_separator_regex = False,
  )

  pages = loader.load_and_split(text_splitter=text_splitter)
  texts = text_splitter.split_documents(pages)

  embeddings = OpenAIEmbeddings()
  docsearch = Chroma.from_documents(texts, embeddings)

  qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(), verbose=True)

  template = """
  We are a {company_type} company looking to cut our emissions through targeting our {target}.
  
  Give me three actionable, realistic to-dos.
  """

  prompt = PromptTemplate(
      input_variables=["company_type","target"],
      template=template,
  )

  final_prompt = prompt.format(company_type=query_params["company_type"], target=query_params["target"])

  return qa.run(final_prompt)