import json
import os
import os.path as osp
from typing import AsyncGenerator, Coroutine, Generator, Union

import requests
import utils

MessageCompletion = dict[str, list[dict[str, dict[str]]]]

self_llm_url = os.environ.get("SELF_LLM_URL")

if self_llm_url is None:
    raise ValueError("SELF_LLM_URL is not set. Please set it to .env file.")


class ChatCompletion:
    @classmethod
    def create(
        cls,
        model: str,
        messages: list[dict[str, str]],
        stream: bool,
        max_tokens: int = 4096,
        **kwargs,
    ) -> Union[Generator[MessageCompletion, None, None], MessageCompletion]:
        s = requests.Session()
        prepared = requests.Request(
            "POST",
            osp.join(self_llm_url, "completions"),
            json={
                "model": model,
                "messages": messages,
                "stream": stream,
                "max_tokens": max_tokens,
                **kwargs,
            },
        ).prepare()

        response = s.send(prepared, stream=stream)
        if stream:
            return (
                utils.convert_to_selfllm_object(i) for i in response.iter_content(1024)
            )
        else:
            return utils.convert_to_selfllm_object(response.content)

    @classmethod
    async def acreate(
        cls,
        model: str,
        messages: list[dict[str, str]],
        stream: bool,
        max_tokens: int = 4096,
        **kwargs,
    ) -> Coroutine[
        MessageCompletion,
        MessageCompletion,
        Union[AsyncGenerator[MessageCompletion, None], MessageCompletion],
    ]:
        pass
