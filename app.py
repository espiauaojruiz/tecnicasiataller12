import streamlit as st

from model import Model
from database import Database
from document import Document

from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Funcion encargada de invocar la funcion definida en el grafo para gestionar la memoria,
# que a su vez es la funcion encargada de invocar el modelo.
def chat(user_message: str):
  config={"configurable": {"thread_id": "1"}}
  response = graph.invoke(
    {
      "messages": [HumanMessage(content=user_message)]
    },
    config,
  )

  return response["messages"][-1].content

# Configuracion del grafo
if "graph" in st.session_state:
  graph = st.session_state.graph
else:
  memory = MemorySaver()
  workflow = StateGraph(MessagesState)
  workflow.add_node("rag", Model.call_model)
  workflow.add_edge(START, "rag")
  graph = workflow.compile(checkpointer=memory)
  st.session_state.graph = graph

st.title("RAG")
with st.sidebar:
  st.title("")
  pdf = st.file_uploader(label='Seleccione archivo.pdf', type="pdf", accept_multiple_files=False)
  button = st.button("Cargar PDF", disabled=True if pdf is None else False)
  if button:
    if pdf:
      with st.spinner("Cargando..."):
        text = Document.read_pdf(pdf)
      st.success("PDF cargado con éxito")

      chroma_client = Database.get_client()
      chroma_collection = Database.get_create_collection("test", chroma_client)

      text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=200)
      chunks = text_splitter.split_text(text)
      embeddings = Model.get_embeddings(chunks)

      chroma_collection.add(
        documents = chunks,
        embeddings = embeddings,
        ids = [pdf.name+str(i) for i in range(len(chunks))],
      )

      pdf.close()

# GUI
if "chat_messages" not in st.session_state:
  st.session_state.chat_messages = []

for chat_message in st.session_state.chat_messages:
  with st.chat_message(chat_message["role"]):
    st.markdown(chat_message["content"])

user_message = st.chat_input("Escribe algo...")

if user_message:
  with st.chat_message("user"):
    st.markdown(user_message)

  st.session_state.chat_messages.append({"role": "user", "content": user_message})

  response = chat(user_message)

  with st.chat_message("assistant"):
    st.markdown(response)

  st.session_state.chat_messages.append({"role": "assistant", "content": response})
