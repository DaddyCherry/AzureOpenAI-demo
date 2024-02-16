# openai==0.28

import os, openai, requests
from dotenv import load_dotenv
load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-08-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY").strip()
openai.api_base = "https://demo-openai231223.openai.azure.com/"
model = "demo-gpt35-turbo"

search_endpoint = "https://demoaisrch240117.search.windows.net"; # Add your Azure AI Search endpoint here
# search_key = os.getenv("AZURE_SEARCH_KEY"); # Add your Azure AI Search admin key here
search_key = 'xvOs1mOx6EjD9535gjaTmNAN7oZkNkGVv33naUAdAIAzSeAqk9fS' # Add your Azure AI Search admin key here
search_index_name = "demoindex2-index"; # Add your Azure AI Search index name here


def setup_byod(deployment_id: str) -> None:
    """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.

    :param deployment_id: The deployment ID for the model to use with your own data.

    To remove this configuration, simply set openai.requestssession to None.
    """

    class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):

        def send(self, request, **kwargs):
            request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            return super().send(request, **kwargs)

    session = requests.Session()

    # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
    session.mount(
        prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
        adapter=BringYourOwnDataAdapter()
    )

    openai.requestssession = session

setup_byod(model)


text_prompt = "I'd like to take a trip to New York. Where should I stay?"


message_text = [{"role": "user", "content": text_prompt}]

completion = openai.ChatCompletion.create(
    messages=message_text,
    deployment_id=model,
    dataSources=[  # camelCase is intentional, as this is the format the API expects
        {
            "type": "AzureCognitiveSearch",
            "parameters": {
                "endpoint": search_endpoint,
                "key": search_key,
                "indexName": search_index_name,
            }
        }
    ]
)
print(completion)