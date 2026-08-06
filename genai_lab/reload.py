from pathlib import Path
import chromadb

db_path = Path(__file__).parent / "chroma_db"
chroma_client = chromadb.PersistentClient(path=str(db_path))

collection = chroma_client.get_collection("support_docs")
print("Stored documents:", collection.count())