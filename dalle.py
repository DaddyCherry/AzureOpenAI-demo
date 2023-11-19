import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-06-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY").strip()
openai.api_base = "https://demo-aoai231005.openai.azure.com/"

response = openai.Image.create(
    prompt='flat illust inside Azure datacenter',
    size='1024x1024',
    n=1
)

print(response)

image_url = response["data"][0]["url"]
print(image_url)