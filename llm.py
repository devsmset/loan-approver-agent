from langchain.chat_models import init_chat_model
import os


def llm():
    return init_chat_model(
        "nvidia/nemotron-3.5-lightning:free",
        model_provider="openai",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["llm_api_key"],
        temperature=0,
    )


if __name__ == "__main__":
    result = llm().invoke("what model are you?")
    print(result)
