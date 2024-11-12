from database import Database
from document import Document
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import SystemMessage

class Model:

  load_dotenv()
  model = ChatOpenAI(model="gpt-4o")

  # Funcion que realiza consultas al modelo
  def call_model(state: MessagesState):
    chroma_client = Database.get_client()
    chroma_collection = Database.get_create_collection("test", chroma_client)

    user_message = state["messages"][-1].content

    reponse_chromadb = chroma_collection.query(query_embeddings = OpenAIEmbeddings().embed_documents([user_message]), n_results = 2)
    documents = reponse_chromadb["documents"][0]

    system_prompt = (f"""
      Eres un asistente de una inmobiliaria quien con ayuda del siguiente contexto
      {Document.format_docs(documents)}, e información adicional que los usuarios idiquen,
      darás respuesta a las preguntas de los usuarios, se conciso y preciso, si no sabes la respuesta
      dí que no sabes, si no entiendes la pregunta pide que la repitan.
    """)

    message = [SystemMessage(content=system_prompt)] + state["messages"]

    response = Model.model.invoke(message)
    
    return {"messages": response}
  
  def get_embeddings(chunks):
    embeddings = OpenAIEmbeddings().embed_documents(chunks)
    return embeddings