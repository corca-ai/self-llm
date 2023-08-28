import os.path as osp
from typing import AsyncGenerator, Coroutine, Generator, Union

import requests
import requests_async
import self_llm
import self_llm.utils as utils

MessageCompletion = dict[str, list[dict[str, dict[str]]]]


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
            osp.join(self_llm.self_llm_url, "completions"),
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
        s = requests_async.Session()
        prepared = requests_async.Request(
            "POST",
            osp.join(self_llm.self_llm_url, "completions"),
            json={
                "model": model,
                "messages": messages,
                "stream": stream,
                "max_tokens": max_tokens,
                **kwargs,
            },
        ).prepare()

        response = await s.send(prepared, stream=stream)
        if stream:
            return (
                utils.convert_to_selfllm_object(i) async for i in response.iter_lines()
            )
        else:
            return utils.convert_to_selfllm_object(response.content)
