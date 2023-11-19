import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-09-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY").strip()
openai.api_base = "https://demo-aoai231005.openai.azure.com/"
model = "gpt-35-turbo-16k"


text_prompt = "GPTは将来AGIになりますか？"

response = openai.ChatCompletion.create(
  engine=model,
  messages = [{"role":"system", "content":"You are a helpful assistant."},
               {"role":"user","content":text_prompt},])

print(response)

res = response['choices'][0]['message']['content']
print(res)