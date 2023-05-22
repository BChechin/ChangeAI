from multidict import MultiDict
from aiogram.utils.web_app import WebAppInitData
from urllib.parse import parse_qs
from typing import Any, Callable
from operator import itemgetter
import hmac
import hashlib
import json

from pathlib import Path

from aiogram import Bot

from db.models import User

from utils.check_webapp_signature import check_webapp_signature

from multidict import MultiDict
from datetime import datetime

from fastapi import APIRouter, Request, Body, Response, status
from fastapi.responses import JSONResponse

from aiogram import Bot

from db.models import User, PaymentPlans, PaymentCurrency, PaymentPeriods

from urllib.parse import parse_qs
import config

router = APIRouter(prefix="/settings")


@router.get("/ping")
async def ping():
    return '<h1>ping</h1>'


@router.post("/setSettings")
async def check_data_handler_1(response=Body(...)):
    # Gets settings from web app
    # weird_data = parse_qs(response.decode('UTF-8'))
    # data = {k: v[0] for k, v in weird_data.items()}
    data = response

    bot = Bot(token=config.TOKEN)

    print(data)

    # if not check_webapp_signature(bot.token, _auth["_auth"]):
    if not check_webapp_signature(bot.token, data["_auth"]):
        # if not check_webapp_signature(bot.token, json.dumps(data)):
        content = {"ok": False}
        return JSONResponse(content=content, status_code=status.HTTP_401_UNAUTHORIZED)

    user = await User.get_or_none(user_id=data["_auth"]["user"]["id"], bot_id=bot.id)

    data.pop("_auth")
    user.settings = data
    await user.save()
    # return json_response(data)
    return {"ok": True}