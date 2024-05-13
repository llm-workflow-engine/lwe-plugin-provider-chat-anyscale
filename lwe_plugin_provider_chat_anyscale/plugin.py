import os
import requests

from langchain_community.chat_models import ChatAnyscale
from langchain_core.pydantic_v1 import Field

from lwe.core.provider import Provider, PresetValue

ANYSCALE_API_BASE = "https://api.endpoints.anyscale.com/v1"
ANYSCALE_DEFAULT_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"


class CustomChatAnyscale(ChatAnyscale):

    @property
    def _llm_type(self):
        return "chat_anyscale"

    model_name: str = Field(default=ANYSCALE_DEFAULT_MODEL, alias="model")
    """Model name to use."""


class ProviderChatAnyscale(Provider):
    """
    Access to Anyscale chat models.
    """

    def __init__(self, config=None):
        super().__init__(config)
        self.models = self.config.get('plugins.provider_chat_anyscale.models') or self.fetch_models()

    def fetch_models(self):
        models_url = f"{ANYSCALE_API_BASE}/models"
        try:
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Bearer {os.environ['ANYSCALE_API_KEY']}",
            }
            response = requests.get(models_url, headers=headers)
            response.raise_for_status()
            models_data = response.json()
            models_list = models_data.get('data')
            if not models_list:
                raise ValueError('Could not retrieve models')
            models = {}
            for model in models_list:
                max_total_tokens = model.get('rayllm_metadata', {}).get('engine_config', {}).get('max_total_tokens')
                model_type = model.get('rayllm_metadata', {}).get('engine_config', {}).get('model_type')
                if max_total_tokens is not None and model_type == 'text-generation':
                    models[model['id']] = {'max_tokens': max_total_tokens}
            return models
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Could not retrieve models: {e}")

    @property
    def default_model(self):
        return ANYSCALE_DEFAULT_MODEL

    @property
    def capabilities(self):
        return {
            "chat": True,
            'validate_models': True,
            "models": self.models,
        }

    def prepare_messages_method(self):
        return self.prepare_messages_for_llm_chat

    def llm_factory(self):
        return CustomChatAnyscale

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
