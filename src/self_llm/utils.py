import json

from self_llm.object import SelfLLMObject


def convert_to_selfllm_object(data: bytes) -> SelfLLMObject:
    return SelfLLMObject(json.loads(data.decode("utf-8")))
