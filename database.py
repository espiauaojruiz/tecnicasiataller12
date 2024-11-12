import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings

class Database:
  def get_client():
    chroma_client = chromadb.PersistentClient(
      path = "db/",
      settings = Settings(),
      tenant = DEFAULT_TENANT,
      database = DEFAULT_DATABASE,
    )
    return chroma_client

  def get_create_collection(collection_name:str, chroma_client:chromadb.Client) -> chromadb.Collection:
    chroma_collection = chroma_client.get_or_create_collection(collection_name)
    return chroma_collection
