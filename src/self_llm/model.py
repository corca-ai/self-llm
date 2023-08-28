import os.path as osp

import requests
import self_llm
import self_llm.utils as utils


class Model:
    @classmethod
    def list(cls) -> list[str]:
        s = requests.Session()
        prepared = requests.Request(
            "GET",
            osp.join(self_llm.self_llm_url, "models"),
        ).prepare()

        response = s.send(prepared)

        return utils.convert_to_selfllm_object(response.content)
