from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain.vectorstores.utils import filter_complex_metadata
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import chroma;
#from langchain_community.embeddings import fastembed;
from langchain_community.embeddings import jina

class ChunkVectorStore:

  def __init__(self) -> None:
    pass

  def split_into_chunks(self, file_path: str):
    doc = PyPDFLoader(file_path).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=10)
    chunks = text_splitter.split_documents(doc)
    #chunks = filter_complex_metadata(chunks)

    return chunks

  def store_to_vector_database(self, chunks):
    return chroma.Chroma.from_documents(documents=chunks, embedding=jina.JinaEmbeddings(
      model_name="jina-embeddings-v2-base-en",
      jina_api_key="jina_259064ef8dba4887970b0f9f0dab5f3bAvL5ngbmBDFOLDVtcxKqZ5wyLY99"
    ))

