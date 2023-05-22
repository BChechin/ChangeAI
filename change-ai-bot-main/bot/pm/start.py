import pprint
from typing import Awaitable
from aiogram import Router, Bot, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


from bot.texts import TranslationTexts as texts
import config

from enum import Enum


from tgtypes import DbUser


from aiogram import Router, F
from aiogram.filters.command import Command


from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from utils.image import get_result, queue_request

from aiogram.filters.callback_data import CallbackData, CallbackQuery

import aiohttp


router = Router()


# class Onboarding(StatesGroup):
#     waiting_for_picture = State()
#     request_queued = State()
class MyCallback(CallbackData, prefix="my"):
    foo: str
    bar: int


@router.message(Command(commands=["start"]))
async def command_start_handler(
    message: types.Message,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    This handler receive messages with `/start` command
    """

    if message.text == "/start":
        print('start handler')
        # Invoke with "/start"
        # await message.answer(texts.HELLO_WORLD())
        webapp = types.WebAppInfo(url=config.WEBAPP_SETTINGS_URL)
        button = types.MenuButtonWebApp(
            type='web_app', text=texts.MENU_BUTTON_WEB_APP_TEXT(), web_app=webapp)
        await bot.set_chat_menu_button(chat_id=message.from_user.id, menu_button=button)

        # await message.answer(message.chat.id)
        # Onboaring begins
        text = texts.START()
        await message.answer(text=text)


@router.message(Command(commands=["help", "help_ru"]))
async def command_help_handler(
    message: types.Message,
    command: CommandObject,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    This handler receive messages with `/help` command
    """
    if command.command == "help":
        # if message.text == "/help":
        # Invoke with "/help"
        await message.answer(texts.HELP())
        return

    if message.text == "/help_ru":
        # Invoke with "/help_ru"
        await message.answer(texts.HELP_RU())


@router.message(Command(commands=["subscription"]))
async def command_subscription_handler(message: types.Message) -> None:
    """
    This handler receives message with '/subscription' command
    """
    await message.answer(text=texts.SUBSCRIPTION_INFO())


# 2. Отмена подписки (По команде /cancel вылезает сообщение с подтверждением отмены (кнопки да и нет), далее при подтверждении посылается нужный запрос в клаунпэйментс (хз, какой, смотри в их доках))
@router.message(Command(commands=["cancel"]))
async def command_cancel_handler(message: types.Message) -> None:
    """
    This handler receive message with '/cancel' command
    """
    webapp = types.WebAppInfo(url=config.WEBAPP_LANDING_URL)
    kb = InlineKeyboardBuilder()
    # Cancels subscription (in cloudpayments docs)
    kb.button(text='yes', callback_data=MyCallback(
        foo="yes", bar="42"))
    # Makes edit of this message to show subscription data and removes buttons
    kb.button(text='no', callback_data=MyCallback(
        foo="no", bar="42"))
    await message.answer(text=texts.CANCEL_SUBSCRIPTION(), reply_markup=kb.as_markup())


# Filter callback by type and value of field :code:`foo`
@router.callback_query(MyCallback.filter(F.foo == "yes"))
async def my_callback_foo(query: CallbackQuery, callback_data: MyCallback):
    auth = aiohttp.BasicAuth(
        'pk_68b34efc94a0c6a0e2247cc16661e', 'f4ecfc9d8e870b88887c84c5f6bb362a')
    url = f"https://api.cloudpayments.ru/subscriptions/find"
    user_id = {"accountId": '431544132'}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, data=user_id, auth=auth) as response:
            user_subscriptions = await response.json()

            url = f"https://api.cloudpayments.ru/subscriptions/cancel"
            subscription_id = user_subscriptions['Model'][-1]['Id']
            user_id = {"Id": subscription_id}
            async with session.post(url=url, data=user_id, auth=auth) as response:
                res = await response.json()
                pprint.pprint(res)
                if res['Success']:
                    await query.message.edit_text(texts.SUBSCRIPTION_WAS_CANCELED())


@router.callback_query(MyCallback.filter(F.foo == "no"))
async def my_callback_foo(query: CallbackQuery, callback_data: MyCallback):
    await query.message.edit_text(texts.SUBSCRIPTION_INFO())


@router.message(Command(commands=["pay"]))
async def command_pay_handler(
    message: types.Message,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    This handler receive messages with `/start` command
    """

    webapp = types.WebAppInfo(url=config.WEBAPP_LANDING_URL)
    kb = InlineKeyboardBuilder()
    kb.button(text='pay', web_app=webapp)
    await message.answer(text='test', reply_markup=kb.as_markup())
    return
    # button = types.MenuButtonWebApp(
    #     type='web_app', text=texts.MENU_BUTTON_TG_LANDING_TEXT(), web_app=webapp)
    # await bot.set_chat_menu_button(chat_id=message.from_user.id, menu_button=button)
    # return


@router.message(F.photo != None)
async def message_image_hander_with_photo(
    message: types.Message,
    bot: Bot,
    dbuser: Awaitable[DbUser]
):
    """
    This handler recieves photo without caption
    """
    user = await dbuser
    user.db.current_image = message.photo[-1].file_id
    await user.db.save()

    if not message.caption:
        text = texts.PHOTO_WITHOUT_CAPTION()
        await message.answer(text=text)
        return

    generation_info = await queue_request(message.caption, bot, user)
    await send_queue_info_message(message, generation_info)

    result = await get_result(generation_info)
    await message.answer_photo(photo=result, caption=texts.GENERATED_BY())


@router.message()
async def message_image_handler(
    message: types.Message,
    state: FSMContext,
    bot: Bot,
    dbuser: Awaitable[DbUser]
) -> None:
    """
    This handler receive caption without photo
    """
    user = await dbuser

    # await bot.download(file=message.photo[-1], destination=Path("./bot/img/new.png"))
    if not user.db.current_image:
        # if exists in db
        text = texts.CAPTION_WITHOUT_PHOTO()
        await message.answer(text=text)

    generation_info = await queue_request(message.text, bot, user)
    await send_queue_info_message(message, generation_info)

    result = await get_result(generation_info)
    await message.answer_photo(photo=result)


async def send_queue_info_message(message: types.Message, generation_info: dict):
    webapp = types.WebAppInfo(url=config.WEBAPP_LANDING_URL)
    kb = InlineKeyboardBuilder()
    kb.button(text='Skip queue', web_app=webapp)
    await message.answer(texts.QUEUE_PUT_IN_REQUEST(**generation_info), reply_markup=kb.as_markup())
