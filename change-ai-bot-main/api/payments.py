from multidict import MultiDict
from datetime import datetime

from fastapi import APIRouter, Request, Body, Response
from aiogram import Bot

from db.models import User, PaymentPlans, PaymentCurrency, PaymentPeriods

from urllib.parse import parse_qs
import config


router = APIRouter(prefix="/payments")


@router.get("/ping")
async def pong():
    return {"response": "pong"}


@router.post('/check')
async def post_cloudpayment_notifications(response=Body(...)):
    weird_data = parse_qs(response.decode('UTF-8'))
    data = {k: v[0] for k, v in weird_data.items()}

    # data: MultiDict = await request.json()
    # print(data)
    # Check amount
    # AccoutId
    print(data)
    print(type(data))
    account_id = data.get('AccountId')
    if account_id == "undefined":
        return {"code": 11}
    # if account_id <= 0:
    #     print('code: 11')
    #     return json_response({"code": 11})

    amount = float(data.get('Amount'))
    if amount != float(8):
        print('code: 12')
        return {"code": 12}
    # if wrong amount => code: 12
    print('code: 0')
    return {"code": 0}


@router.post('/pay')
async def post_cloudpayment_notifications(response=Body(...)):
    weird_data = parse_qs(response.decode('UTF-8'))
    data = {k: v[0] for k, v in weird_data.items()}
    bot = Bot(token=config.TOKEN)

    # print(response.app["bot"].decode('utf-8'))

    payment_plan = PaymentPlans.basic
    payment_period = PaymentPeriods.month
    currency = PaymentCurrency.USD
    payment_amount = data.get('Amount')
    last_payment_date = data.get('DateTime')
    ip_city = data.get('IpCity')
    description = data.get('Description')
    account_id = data.get('AccountId')

    user = await User.get_or_none(user_id=account_id, bot_id=bot.id)

    user.payment_plan = payment_plan
    user.payment_period = payment_period
    user.currency = currency
    user.payment_amount = float(payment_amount)

    date_time = datetime.strptime(last_payment_date, '%Y-%m-%d %H:%M:%S')

    user.last_payment_date = date_time

    await user.save()

    text = '\n'.join([
        f'payment plan: {payment_plan}',
        f'payment period: {payment_plan}',
        f'currency: {currency}',
        f'payment amount: {payment_amount}',
        f'last payment date: {last_payment_date}',
        f'description: {description}',
        f'ip city: {ip_city}',
        f'last payment date: {last_payment_date}',
        f'account id: {account_id}'
    ])
    await bot.send_message(chat_id="-1001844564618", text=text)

    await bot.send_message(chat_id=account_id, text="Your purchase was successful!")

    print('pay')
    return {"ok": True}