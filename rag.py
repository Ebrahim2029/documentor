from chunk_vector_store import ChunkVectorStore as cvs
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama

class Rag:

  vector_store = None
  retriever = None
  chain = None

  def __init__(self) -> None:
    self.csv_obj = cvs()
    self.prompt = PromptTemplate.from_template(
      """
      <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context
      to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
        maximum and keep the answer concise. [/INST] </s>
      [INST] Question: {question}
      Context: {context}
      Answer: [/INST]
      """
    )
    #self.model = ChatOllama(model="mistral")
    self.model = ChatOllama( model="llama3.1", temperature=0)

  def set_retriever(self):
    self.retriever = self.vector_store.as_retriever(
      search_type="similarity_score_threshold",
      search_kwargs={
        "k": 3,
        "score_threshold": 0.5,
      },
    )

  # Augment the context to original prompt.
  def augment(self):
    self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
    | self.prompt
    | self.model
    | StrOutputParser())


  # Generate the response.
  def ask(self, query: str):
    if not self.chain:
      return "Please upload a PDF file for context"

    return self.chain.invoke(query)

  # Stores the file into vector database.
  def feed(self, file_path: str):
    chunks = self.csv_obj.split_into_chunks(file_path)
    self.vector_store = self.csv_obj.store_to_vector_database(chunks)

    self.set_retriever()
    self.augment()


  def clear(self):
    self.vector_store = None
    self.chain = None
    self.retriever = None


""" path_source= "test_1_pdf_one_page.pdf"
obj = Rag()
obj.feed(path_source)
while(True):

  ask_qu =input("ask : ")
  if ask_qu == "stop":
    break
  else:
    resualt = obj.ask(ask_qu)
    print(resualt) """