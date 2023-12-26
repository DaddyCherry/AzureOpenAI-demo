import os, openai
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.callbacks import get_openai_callback

from langchain.chat_models import AzureChatOpenAI

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader


openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY").strip()
openai.api_base = "https://demo-openai231223.openai.azure.com/"


aoai = AzureChatOpenAI(
    client=None,
    deployment_name="demo-gpt35-turbo",
    openai_api_base=openai.api_base,
    openai_api_version=openai.api_version or "",
    openai_api_key=openai.api_key or "",
    temperature=0,
    request_timeout=180,
)


loader = TextLoader('./some_fictional_story.txt')
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(
    client=None,
    engine="demo-text-embedding-ada-002",
    chunk_size=1,
    openai_api_key=openai.api_key,
)

db = FAISS.from_documents(documents=docs, embedding=embeddings)

doc_chain = load_qa_chain(
    aoai,
    chain_type="map_reduce",
)

condense_question_chain = LLMChain(llm=aoai, prompt=CONDENSE_QUESTION_PROMPT)

qa = ConversationalRetrievalChain(
    retriever=db.as_retriever(),
    combine_docs_chain=doc_chain,
    question_generator=condense_question_chain,
    return_source_documents=True,
    verbose=True,
)

with get_openai_callback() as cb:
    content = qa(
        {
            "question": "What did Lily eat?",
            # history is consist by tuple_list
            "chat_history": [],
            # Return results with search distance greater than or equal to 0.9
            "vectordbkwargs": {"search_distance": 0.9},
        }
    )
    print("successful_requests: ", cb.successful_requests)
    print("total_tokens: ", cb.total_tokens)
    print("prompt_tokens: ", cb.prompt_tokens)
    print("completion_tokens: ", cb.completion_tokens)
    print("total_cost: ", cb.total_cost)
    print("content", content)