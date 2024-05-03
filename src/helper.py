from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

#Extract data from the PDF
def load_pdf(data):
    """
    Load PDF files from the given directory.

    Args:
        data (str): The directory path where the PDF files are located.

    Returns:
        List[Document]: A list of Document objects representing the loaded PDF files.
    """
    loader = DirectoryLoader(data,
                    glob="*.pdf",
                    loader_cls=PyPDFLoader)
    
    documents = loader.load()

    return documents

#Create text chunks
def text_split(extracted_data):
    """
    Splits the given extracted data into text chunks using the RecursiveCharacterTextSplitter.

    Args:
        extracted_data (List[Document]): The extracted data to be split into text chunks.

    Returns:
        List[Document]: The list of text chunks obtained after splitting the extracted data.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks

#download embedding model
def download_hugging_face_embeddings():
    """
    Downloads the Hugging Face embeddings for the given model.

    Returns:
        HuggingFaceEmbeddings: The Hugging Face embeddings object.
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings