import os, openai
from langchain.callbacks import get_openai_callback
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage


openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY").strip()
openai.api_base = "https://demo-openai231223.openai.azure.com/"


with get_openai_callback() as cb:
    chat = AzureChatOpenAI(
        client=None,
        deployment_name="demo-gpt35-turbo",
        openai_api_base=openai.api_base,
        openai_api_version=openai.api_version or "",
        openai_api_key=openai.api_key or "",
        temperature=0,
        request_timeout=180,
    )
    content = chat(
        [
            SystemMessage(
                content="""You are an AI assistant that helps people find information."""
            ),
            HumanMessage(content="このレストランは素晴らしい。食事も最高だった。"),
            AIMessage(content="Positive"),
            HumanMessage(content="非常にがっかりした。料理はぬるく、味もいまいちだった。"),
            AIMessage(content="Negative"),
            HumanMessage(content="サービスは良かったが、料理が期待ほどではなかった。"),
        ]
    )
    print("successful_requests: ", cb.successful_requests)
    print("total_tokens: ", cb.total_tokens)
    print("prompt_tokens: ", cb.prompt_tokens)
    print("completion_tokens: ", cb.completion_tokens)
    print("total_cost: ", cb.total_cost)
    print("content", content)