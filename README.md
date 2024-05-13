# LLM Workflow Engine (LWE) Chat Anyscale Provider plugin

Chat Anyscale Provider plugin for [LLM Workflow Engine](https://github.com/llm-workflow-engine/llm-workflow-engine)

Access to [Anyscale](https://docs.anyscale.com) models.

## Installation

### Export API key

Grab an Anyscale API key from [https://app.endpoints.anyscale.com/credentials](https://app.endpoints.anyscale.com/credentials)

Export the key into your local environment:

```bash
export ANYSCALE_API_KEY=<API_KEY>
```

### From packages

Install the latest version of this software directly from github with pip:

```bash
pip install git+https://github.com/llm-workflow-engine/lwe-plugin-provider-chat-anyscale
```

### From source (recommended for development)

Install the latest version of this software directly from git:

```bash
git clone https://github.com/llm-workflow-engine/lwe-plugin-provider-chat-anyscale.git
```

Install the development package:

```bash
cd lwe-plugin-provider-chat-anyscale
pip install -e .
```

## Configuration

Add the following to `config.yaml` in your profile:

```yaml
plugins:
  enabled:
    - provider_chat_anyscale
    # Any other plugins you want enabled...
  # THIS IS OPTIONAL -- By default the plugin loads all model data via an API
  # call on startup. This does make startup time longer.
  # You can instead provide a 'models' object here with the relevant data, and
  # It will be used instead of an API call.
  provider_chat_anyscale:
    models:
      # 'id' parameter of the model as it appears in the API.
      "meta-llama/Meta-Llama-3-8B-Instruct":
        # The only parameter, and it's required.
        max_tokens: 8192
```

## Usage

From a running LWE shell:

```
/provider anyscale
/model model meta-llama/Llama-2-70b-chat-hf
```
