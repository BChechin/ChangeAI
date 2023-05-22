import PIL.Image
import io
import aiohttp
from PIL.Image import Image
from pathlib import Path
from typing import Dict, List, Optional, Tuple, ClassVar, Type
import uuid


from marshmallow_dataclass import dataclass
from marshmallow import Schema


DEFAULT_PROMPT_GUIDANCE_SCALE = 7.0  # noqa
DEFAULT_IMAGE_GUIDANCE_SCALE = 1.5  # noqa
DEFAULT_NUM_INFERENCE_STEPS = 20  # noqa

# generate_image_blocking
GENERATE_IMAGE_BLOCKING_HANDLE = "generate_image_blocking"
GENERATE_IMAGE_HANDLE = "generate_image"
GET_IMAGE_HANDLE = "get_image"
GET_STATUS_HANDLE = "get_status"


def serialize_image(image: Image) -> dict:
    return {
        "data": image.tobytes().decode("latin1"),
        "size": image.size,
        "mode": image.mode
    }


@dataclass
class ImageGeneratorRequest:
    prompt: str
    image_mode: str  # "RGB"
    image_size: Tuple[int, int]
    image_data: str
    num_images: int = 1
    num_inference_steps: int = DEFAULT_NUM_INFERENCE_STEPS
    image_guidance_scale: float = DEFAULT_IMAGE_GUIDANCE_SCALE
    prompt_guidance_scale: float = DEFAULT_PROMPT_GUIDANCE_SCALE
    id: Optional[str] = None
    user: Optional[str] = None
    Schema: ClassVar[Type[Schema]] = Schema

    def __post_init__(self):
        if self.id is None:
            self.id = self.generate_id()

    @staticmethod
    def generate_id():
        # todo: use dataclasses field uuid to circumvent conversion to str.
        return str(uuid.uuid4())

    def to_json(self) -> dict:
        return self.Schema().dump(self)

    def from_json(self, source: dict):
        return self.Schema().load(source)

    def dumps(self) -> str:
        return self.Schema().dumps(self)

    @classmethod
    def loads(cls, source: str):
        return cls.Schema().loads(source)


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def generate_image(
            self,
            prompt: str, image: Image,
            num_iterations=DEFAULT_NUM_INFERENCE_STEPS,
            image_guidance_scale=DEFAULT_IMAGE_GUIDANCE_SCALE,
            prompt_guidance_scale=DEFAULT_PROMPT_GUIDANCE_SCALE
    ) -> dict:  # request id
        image_dict = serialize_image(image)
        print(prompt)
        request = ImageGeneratorRequest(
            prompt=prompt,
            image_mode=image_dict["mode"],
            image_size=image_dict["size"],
            image_data=image_dict["data"],
            num_inference_steps=num_iterations,
            image_guidance_scale=image_guidance_scale,
            prompt_guidance_scale=prompt_guidance_scale
        )
        # send request
        # response = aiohttp.pos .post(
        #     f"{self.base_url}/{GENERATE_IMAGE_HANDLE}", json=request.to_json())
        url = f"{self.base_url}/{GENERATE_IMAGE_HANDLE}"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=request.to_json()) as response:
                # return request id
                print(await response.text())
                print(response.status)
                generation_info = await response.json()
                generation_info['orig_image'] = image
                generation_info['request'] = request
                return generation_info

    async def get_status(self, request_id: str) -> dict:
        # return "pending", "running", "done", "error"
        url = f"{self.base_url}/{GET_STATUS_HANDLE}/{request_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # return request id
                # print(await response.text())
                return await response.json()
            
    async def get_result(self, request_id: str) -> Image:
        # return None if not done
        # raise exception if error    
        url = f"{self.base_url}/{GET_IMAGE_HANDLE}/{request_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                image = PIL.Image.open(io.BytesIO(await response.content.read()))
        return image

    # def generate_image_blocking(
    #         self,
    #         prompt: str, image: Image,
    #         num_iterations=DEFAULT_NUM_INFERENCE_STEPS,
    #         image_guidance_scale=DEFAULT_IMAGE_GUIDANCE_SCALE,
    #         prompt_guidance_scale=DEFAULT_PROMPT_GUIDANCE_SCALE
    # ) -> dict:  # request id
    #     image_dict = serialize_image(image)
    #     request = ImageGeneratorRequest(
    #         prompt=prompt,
    #         image_mode=image_dict["mode"],
    #         image_size=image_dict["size"],
    #         image_data=image_dict["data"],
    #         num_inference_steps=num_iterations,
    #         image_guidance_scale=image_guidance_scale,
    #         prompt_guidance_scale=prompt_guidance_scale
    #     )
        
    #     response = requests.get(
    #         f"{self.base_url}/{GENERATE_IMAGE_BLOCKING_HANDLE}", data=request.dumps())
    #     # return request id
    #     return response.json()
