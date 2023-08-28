import os

from self_llm.engine import ChatCompletion
from self_llm.model import Model

self_llm_url = os.environ.get("SELF_LLM_URL")

__all__ = ["ChatCompletion", "Model", "self_llm_url"]
