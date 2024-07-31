from fastapi import Request
import re
from urllib.parse import unquote
from typing import Union

def call_parameters_decoder(string: str) -> dict:
    arr = string.split("&")

    res = {}

    for param in arr:
        key, value = param.split('=')
        key = unquote(key)
        value = unquote(value)
        keys = list(filter(bool, re.split("[\[\]]",key)))

        last_dict = res

        for i in range(len(keys)):
            if (i+1==len(keys)):
                last_dict[keys[i]] = value
            else:
                new = {}
                last_dict[keys[i]] = new
                last_dict = new

    return res


async def decode_body_request(request: Request) -> Union[dict, None]:
    string = str(await request.body())[2:-1]
    if string != "":
        return call_parameters_decoder(string)
    else:
        return None