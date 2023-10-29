from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import secret
from langchain.prompts import PromptTemplate

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer optimistically, and make sure you provide actionable insights for a climate-conscious company:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

loader = PyPDFLoader("../source_docs/MNReport.pdf")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(openai_api_key=secret.OPENAI_API_KEY)
docsearch = Chroma.from_documents(texts, embeddings)

chain_type_kwargs = {"prompt": PROMPT}
qa = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=secret.OPENAI_API_KEY), chain_type="stuff", retriever=docsearch.as_retriever(), chain_type_kwargs=chain_type_kwargs, verbose=True)

query = "What is Minnesota's biggest concern with reducing greenhouse gas emissions?"
answers = qa.run(query)
print(answers)