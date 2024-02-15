#openai==1.7.2

import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("DALLE_DEMO_KEY").strip()

client = AzureOpenAI(
    api_version="2023-12-01-preview",
    azure_endpoint="https://demo-dalle.openai.azure.com",
    api_key=api_key,
)

result = client.images.generate(
    model="Dalle3", # the name of your DALL-E 3 deployment
    prompt="ねこたぬきキャラクター",
    n=1
)

image_url = json.loads(result.model_dump_json())['data'][0]['url']
print(image_url)