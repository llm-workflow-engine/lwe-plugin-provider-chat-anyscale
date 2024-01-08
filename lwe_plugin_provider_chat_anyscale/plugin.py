from langchain_community.chat_models import ChatAnyscale

from lwe.core.provider import Provider, PresetValue

ANYSCALE_DEFAULT_MODEL = "meta-llama/Llama-2-7b-chat-hf"


class ProviderChatAnyscale(Provider):
    """
    Access to Anyscale chat models.
    """

    @property
    def capabilities(self):
        return {
            "chat": True,
            'validate_models': True,
            'models': {
                'meta-llama/Llama-2-7b-chat-hf': {
                    'max_tokens': 4096,
                },
                'meta-llama/Llama-2-13b-chat-hf': {
                    'max_tokens': 4096,
                },
                'meta-llama/Llama-2-70b-chat-hf': {
                    'max_tokens': 4096,
                },
                'codellama/CodeLlama-34b-Instruct-hf': {
                    'max_tokens': 4096,
                },
                'mistralai/Mistral-7B-Instruct-v0.1': {
                    'max_tokens': 131072,
                },
                'HuggingFaceH4/zephyr-7b-beta': {
                    'max_tokens': 131072,
                },
            }
        }

    @property
    def default_model(self):
        return ANYSCALE_DEFAULT_MODEL

    def llm_factory(self):
        return ChatAnyscale

    def customization_config(self):
        return {
            "verbose": PresetValue(bool),
            "model_name": PresetValue(str, options=self.available_models),
            "temperature": PresetValue(float, min_value=0.0, max_value=2.0),
            "openai_api_key": PresetValue(str, include_none=True, private=True),
            "request_timeout": PresetValue(int),
            "max_retries": PresetValue(int, 1, 10),
            "n": PresetValue(int, 1, 10),
            "max_tokens": PresetValue(int, include_none=True),
            "model_kwargs": {
                "top_p": PresetValue(float, min_value=0.0, max_value=1.0),
                "presence_penalty": PresetValue(float, min_value=-2.0, max_value=2.0),
                "frequency_penalty": PresetValue(float, min_value=-2.0, max_value=2.0),
                "logit_bias": dict,
                "stop": PresetValue(str, include_none=True),
                "user": PresetValue(str),
                "functions": None,
                "function_call": None,
            },
        }
