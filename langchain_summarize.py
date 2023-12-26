import os, openai
from langchain import PromptTemplate
from langchain.callbacks import get_openai_callback
from langchain.chat_models import AzureChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain


openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY").strip()
openai.api_base = "https://demo-openai231223.openai.azure.com/"


with open('./some_long_document.txt', 'r') as file:
    long_text = file.read()

aoai = AzureChatOpenAI(
    client=None,
    deployment_name="demo-gpt35-turbo",
    openai_api_base=openai.api_base,
    openai_api_version=openai.api_version or "",
    openai_api_key=openai.api_key or "",
    temperature=0,
    request_timeout=180,
)

text_splitter = CharacterTextSplitter(chunk_size=1000)
texts = text_splitter.split_text(long_text)
docs = [Document(page_content=t) for t in texts]

map_prompt = PromptTemplate(
    input_variables=["text"],
    template="""Please summarize the following sentences.

{text}""",
)

combine_prompt = PromptTemplate(
    input_variables=["text"],
    template="""Please summarize the following sentences.

{text}""",
)

chain = load_summarize_chain(
    aoai,
    chain_type="map_reduce",
    map_prompt=map_prompt,
    combine_prompt=combine_prompt,
    verbose=True,
)


with get_openai_callback() as cb:
    content = chain.run(docs)
    print("successful_requests: ", cb.successful_requests)
    print("total_tokens: ", cb.total_tokens)
    print("prompt_tokens: ", cb.prompt_tokens)
    print("completion_tokens: ", cb.completion_tokens)
    print("total_cost: ", cb.total_cost)
    print("content", content)