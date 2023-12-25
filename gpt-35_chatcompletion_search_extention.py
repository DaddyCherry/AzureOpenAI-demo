import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY").strip()
openai.api_base = "https://demo-openai231223.openai.azure.com/"
azure_search_key = os.getenv("AZURE_SEARCH_KEY").strip()
model = "demo-gpt35-turbo"


text_prompt = "I'd like to take a trip to New York. Where should I stay?"

response = openai.ChatCompletion.create(
  engine=model,
  messages = [{"role":"system", "content":"You are a helpful assistant."},
               {"role":"user","content":text_prompt}],
  
  dataSources = [
    {
      "type": "AzureCognitiveSearch",
      "parameters": {
        "endpoint": "https://demosrch231225std.search.windows.net",
        "key": os.getenv("AZURE_SEARCH_KEY").strip(),
        "indexName": "demoindex2",
      }
    }
  ]
)

print(response)

res = response['choices'][0]['message']['content']
print(res)