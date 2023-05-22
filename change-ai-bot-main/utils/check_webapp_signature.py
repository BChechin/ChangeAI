from aiogram.utils.web_app import WebAppInitData
from typing import Any, Callable
from operator import itemgetter
import hmac
import hashlib
import json


def check_webapp_signature(token: str, init_data: str) -> bool:
    """
    Check incoming WebApp init data signature

    Source: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app

    :param token: bot Token
    :param init_data: data from frontend to be validated
    :return:
    """
    try:
        parsed_data = dict(init_data)
    except ValueError:  # pragma: no cover
        # Init data is not a valid query string
        return False
    if "hash" not in parsed_data:
        # Hash is not present in init data
        return False
    hash_ = parsed_data.pop("hash")

    data_check_string = "\n".join(
        f"{k}={v}".replace(': ', ':').replace(', ', ',').replace("\'", '\"') for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(
        key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256)
    calculated_hash = hmac.new(
        key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()
    print('hash_', hash_)
    print('data_check_string', data_check_string)
    print('calculated_hash', calculated_hash)
    return calculated_hash == hash_


def parse_webapp_init_data(
    init_data: str,
    *,
    loads: Callable[..., Any] = json.loads,
) -> WebAppInitData:
    """
    Parse WebApp init data and return it as WebAppInitData object

    This method doesn't make any security check, so you shall not trust to this data,
    use :code:`safe_parse_webapp_init_data` instead.

    :param init_data: data from frontend to be parsed
    :param loads:
    :return:
    """
    result = {}
    for key, value in init_data:
        if (value.startswith("[") and value.endswith("]")) or (
            value.startswith("{") and value.endswith("}")
        ):
            value = loads(value)
        result[key] = value
    return WebAppInitData(**result)


def safe_parse_webapp_init_data(
    token: str,
    init_data: str,
    *,
    loads: Callable[..., Any] = json.loads,
) -> WebAppInitData:
    """
    Validate raw WebApp init data and return it as WebAppInitData object

    Raise :obj:`ValueError` when data is invalid

    :param token: bot token
    :param init_data: data from frontend to be parsed and validated
    :param loads:
    :return:
    """
    if check_webapp_signature(token, init_data):
        return parse_webapp_init_data(init_data, loads=loads)
    raise ValueError("Invalid init data signature")
