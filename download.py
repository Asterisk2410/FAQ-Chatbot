from huggingface_hub import hf_hub_download
from llama_cpp import Llama


model_name_or_path =  'TheBloke/Llama-2-7B-Chat-GGML'
model_basename = 'llama-2-7b-chat.ggmlv3.q4_0.bin'

model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)

print(model_path)
