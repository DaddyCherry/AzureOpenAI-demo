import os
from openai import AzureOpenAI
from dotenv import load_dotenv


load_dotenv()



client = AzureOpenAI(
  azure_endpoint = "https://demoaoai230213.openai.azure.com/", 
  api_key=os.getenv("AZURE_OPENAI_KEY"),  
  api_version="2024-02-15-preview"
)

user_msg = 'Azureで最も最新のテクノロジーは何でしょうか？'

message_text = [
    {"role":"system","content":"You are an AI assistant that helps people find information."},
    {"role":"user","content":user_msg},
    ]

completion = client.chat.completions.create(
  model="demo-gpt-35-turbo", # model = "deployment_name"
  messages = message_text,
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None
)


print(completion.choices[0].message.content)
