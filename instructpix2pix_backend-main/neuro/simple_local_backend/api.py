# Python fastapi with one handle: generate_image(prompt, image, num_iterations)

# fastapi example:
#
from fastapi import FastAPI

from sd_utils import setup_pix2pix, generate_img2img

app = FastAPI()


class Api:
    def __init__(self, pipe):
        self.app = FastAPI()
        # self.setup()
        self.pipe = pipe

    def setup(self):
        pass

    #     self.app.get('/generate_image')(self.generate_image)

    def generate_image(self, prompt, image, num_iterations=20, image_guidance_scale=1.5):
        # todo: scale image properly, using Ilya's code
        return generate_img2img(prompt=prompt, image=image, pipe=self.pipe, num_inference_steps=num_iterations,
                                image_guidance_scale=image_guidance_scale)


# def generate_image(image, prompt, )-> PIL.Image:
#
#
# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: bool = None
#
#
# @app.get("/")
# async def root():

#     return {"message": "Hello World"}
#
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: str = None):


if __name__ == '__main__':
    # Launch api
    pipe = setup_pix2pix()
    api = Api(pipe)
    api.setup()
