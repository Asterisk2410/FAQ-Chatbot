from src.helper import load_pdf, text_split, download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from dotenv.main import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
dataset = r"C:\Users\Admin\Desktop\Aster\Chatbot-Llama2\data"

extracted_data = load_pdf(dataset)
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()
index_name = "chat"

client = PineconeVectorStore(index_name=index_name,embedding=embeddings, pinecone_api_key=PINECONE_API_KEY)

docsearch=PineconeVectorStore.from_texts([t.page_content for t in text_chunks], embeddings, index_name=index_name)