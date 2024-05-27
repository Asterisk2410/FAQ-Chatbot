from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone.vectorstores import PineconeVectorStore
from langchain.prompts import PromptTemplate
from langchain_community.llms import ctransformers
from langchain.chains.retrieval_qa.base import RetrievalQA
from dotenv.main import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
index_name = "chat"
embeddings = download_hugging_face_embeddings()

client = PineconeVectorStore(index_name=index_name,embedding=embeddings, pinecone_api_key=PINECONE_API_KEY)

docsearch=PineconeVectorStore.from_existing_index(index_name, embeddings)

#prompt_template from src/prompt.py
PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"]) 

chain_type_kwargs={"prompt": PROMPT}

llm=ctransformers.CTransformers(model=r"model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",
                  config={'max_new_tokens':512,
                          'temperature':0.7})

qa=RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=docsearch.as_retriever(search_kwargs={'k': 5}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs)


@app.route("/")
def index():
    """
    Route decorator for the root URL ("/") that defines a function named "index".
    This function returns the rendered template "chat.html".
    """
    return render_template('head.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    """
    A function that handles the chat functionality based on user input, performs a query, and returns the response.
    """
    msg = request.form["msg"]
    input = msg
    print(input)
    result=qa({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])

if __name__ == '__main__':
    print('jmd shree ganesha')
    app.run(host="0.0.0.0", port= 8080, debug= True)