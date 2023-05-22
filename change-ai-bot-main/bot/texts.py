from typing import Union, Callable
from aiogram.utils.i18n import gettext, lazy_gettext


def _(text: str):
    def getargstranslation(**kwargs):
        return gettext(text).format(**kwargs)
    return getargstranslation


def __(text: str, text_plural: str):
    """
    Use keyword number to automatically substitude number
    """
    def getnumtranslation(number: int):
        return gettext(text, text_plural, number).format(number=number)
    return getnumtranslation


class TranslationTexts:
    HELLO_WORLD = _("Hello, world!")
    HELLO_WORLD_PLURALIZATION = __(
        "Hello, {number} world!", "Hello, {number} worlds!")
    HELLO_WORLD_PARAMS = _("{hello_text}, world!")
    HELLO_WORLD_PARAMS_PLURALIZATION = _("{hello_text}, {worlds_plural}!")
    WORLDS_PLURAL = __("{number} world", "{number} worlds!")

    MENU_BUTTON_WEB_APP_TEXT = _("Settings")
    MENU_BUTTON_TG_LANDING_TEXT = _("Payment")

    GREETINGS = _("""
Hi Vladimir Nazarov!
TL;DR: Send an image, tell what to do with it.
Some prompts work better than others. See examples at @BestChangeAi

This bot changes the image you send according to the prompt you specify.
How to use the bot:
1) Send a photo, in the caption of the image specify how to change it
2) Then you can just write what you want to change
(or use /imagine prompt command)
- the bot will apply it to the last image you sent

P.S. For instructions in Russian, use /help_ru""")

    HELP = _("""
TL;DR: Send an image, tell what to do with it.
Some prompts work better than others. See examples at @BestChangeAi

This bot changes the image you send
How to use the bot:
1) Send a photo, in the caption of the image, specify how to change it
2) Then you can just write what you want to change
- the bot will apply it to the last image you sent""")

    HELP_RU = _("""
TL;DR: Шли фотку, говори что с ней делать
Некоторые инструкции работают лучше других. Примеры для вдохновения -  @BestChangeAi

Этот бот изменяет присланное вами изображение согласно вашей инструкции
Как пользоваться ботом:
1) Пришлите фото, в подписи к изображению укажите как его изменить
2) Дальше можно просто писать, что хотите изменить 
- бот будет применять его к последнему присланному вами изображению
(Если не работает на русском - пробуйте на английском)""")

    START = _('''
• Hi, send me a picture that you want to change

Tip: I work best with photos of humans''')

    PHOTO_WITHOUT_CAPTION = _("""
Now send me an instruction of what you want to change

Example: Make him a clown
More examples: @BestChangeAi""")

    CAPTION_WITHOUT_PHOTO = _("""
I can only change images. To continue, please send me an image you want to change.

Tip: you can see examples of my work in @BestChangeAi""")

    QUEUE_PUT_IN_REQUEST = _("""
Your request was placed in the queue

Position: {position_in_queue}/35
Estimated time: 5:13

Tip: visit @BestChangeAi for new ideas""")

    GENERATED_BY = _("""Сгенерировано через Change Image AI (https://t.me/changeaibot?start=12345)
Лучшие результаты Change AI (https://t.me/+blF8NM5H-8YyNTI6)""")

    SUBSCRIPTION_INFO = _("""Hello! Your subscription to our app is set to expire in 5 days.

If you would like to renew your subscription or have any questions about your account, please visit your account settings or contact our customer support team.""")

    CANCEL_SUBSCRIPTION = _("""Are you sure you want to cancel subscription?""")

    SUBSCRIPTION_WAS_CANCELED = _("""Your subscription was canceled.""")