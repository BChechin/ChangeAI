from enum import Enum
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from aiogram import Router, Bot, types
import asyncio

from tgtypes import DbUser

from utils.image.image_generator import ImageGeneratorRequest, Client
from utils.image.img_utils import print_result
from utils.translator import translate


import config

client = Client(config.MOCK_SERVER_URL)


class GenerationStage(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
    MISSING = "MISSING"


def enums_are_equal(e1, e2):
    """
    Fix for enum comparison bug.
    Reference: https://stackoverflow.com/questions/30733271/importing-with-package-name-breaking-enum-comparison-in-python
    For some reason this happens with marshmallow serialisation
    :param e1:
    :param e2:
    :return:
    """
    if isinstance(e1, Enum):
        e1 = e1.value
    if isinstance(e2, Enum):
        e2 = e2.value
    return e1 == e2


async def edit_image(bytesio: BytesIO, photo: types.PhotoSize, caption: str, settings: dict) -> BytesIO:
    img = Image.open(BytesIO(bytesio.getvalue()))
    # res_image = img
    # generate image
    translated_caption = await translate(text=caption)
    print(caption, translated_caption)

    sample_response = await client.generate_image(
        prompt=translated_caption,
        image=img,
        prompt_guidance_scale=settings.get('text_cfg', 7.5),
        image_guidance_scale=settings.get('image_cfg', 1.5),
        num_iterations=settings.get('sampling_steps', 20)
    )
    return sample_response
    # print('PRINT: ', await client.get_status(sample_response['request_id']))

    # todo: create smart async wait algorithm based on queue size  - wait time ~ 1/3 of what it could take. So ~ == 1 op / sec


async def wait_image(generation_info: dict):
    '''Waits for photo editing to be finished'''
    while not enums_are_equal((await client.get_status(generation_info['request_id']))["stage"], GenerationStage.FINISHED):
        await asyncio.sleep(1)

    return await client.get_result(generation_info['request_id'])


async def queue_request(caption: str | None, bot: Bot, user: DbUser):
    image_bytes = BytesIO()
    await bot.download(file=user.db.current_image, destination=image_bytes)

    settings = user.db.settings
    # print(settings)

    edit_image_response = await edit_image(image_bytes, user.db.current_image, caption, settings)
    return edit_image_response


async def get_result(generation_info: dict):
    result_image = await wait_image(generation_info=generation_info)
    # Get settings from database
    data: ImageGeneratorRequest = generation_info["request"]
    image: Image = generation_info["orig_image"]
    double_image = print_result(
        orig=image,
        transformed=result_image,
        prompt=data.prompt,
        prompt_cfg=data.prompt_guidance_scale,
        image_cfg=data.image_guidance_scale)

    edited_image_bytes = BytesIO()
    double_image.save(edited_image_bytes, 'PNG')

    file = BytesIO(edited_image_bytes.getvalue()).read()

    # media = URLInputFile("https://www.python.org/static/community_logos/python-powered-h-140x182.png",
    #                      filename="python-logo.png")
    media = types.BufferedInputFile(file=file, filename="file")
    return media
    await message.answer_photo(photo=media)
