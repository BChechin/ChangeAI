import PIL
import PIL.Image
import PIL.ImageOps
import logging
import re
import requests
from PIL.Image import Image
# Enable logging
from diffusers import StableDiffusionPipeline
from enum import Enum
from typing import List

logger = logging.getLogger(__name__)


class SD_Env(Enum):
    MacBookM1 = "m1"
    GCP_nvidia = "t4"


def setup_sd(sd_env: SD_Env = SD_Env.MacBookM1):
    logger.info("Setting up basic SD model")
    # make sure you're logged in with `huggingface-cli login`
    from diffusers import StableDiffusionPipeline

    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    logger.info("SD model loaded, setting up pipe")
    if sd_env == SD_Env.GCP_nvidia:
        pipe = pipe.to("cuda")
    elif sd_env == SD_Env.MacBookM1:
        pipe = pipe.to("mps")

    # Recommended if your computer has < 64 GB of RAM
    pipe.enable_attention_slicing()
    return pipe


def download_image(url: str) -> Image:
    image = PIL.Image.open(requests.get(url, stream=True).raw)
    image = PIL.ImageOps.exif_transpose(image)
    image = image.convert("RGB")
    return image


def setup_pix2pix(sd_env: SD_Env = SD_Env.GCP_nvidia) -> StableDiffusionPipeline:
    logger.info("Setting up img2img model")
    if sd_env == SD_Env.MacBookM1:
        def mock_pipe(prompt, image, **kwargs):
            namespace = lambda _: _
            namespace.images = [image]
            return namespace

        return mock_pipe
    import torch
    # noinspection PyUnresolvedReferences
    from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler
    model_id = "timbrooks/instruct-pix2pix"
    logger.info("Loading Pix2Pix model...")
    pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(
        model_id, torch_dtype=torch.float16,
        safety_checker=None)
    logger.info("Pix2Pix Model loaded, setting up pipe and scheduler")
    pipe.to("cuda")
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    logger.info("Pix2Pix Model ready")
    # Recommended if your computer has < 64 GB of RAM
    pipe.enable_attention_slicing()
    return pipe


DEFAULT_PROMPT_GUIDANCE_SCALE = 7.0
DEFAULT_IMAGE_GUIDANCE_SCALE = 1.5
DEFAULT_NUM_INFERENCE_STEPS = 20


def generate_img2img(
        prompt: str,
        image: PIL.Image,
        pipe: StableDiffusionPipeline,
        num_images: int = 1,
        num_inference_steps=DEFAULT_NUM_INFERENCE_STEPS,
        image_guidance_scale: float = DEFAULT_IMAGE_GUIDANCE_SCALE,
        prompt_guidance_scale: float = DEFAULT_PROMPT_GUIDANCE_SCALE
) -> List[Image]:
    """
    Generate an image from a prompt and an image
    :param prompt:make him a medieval knight
    :param image:
    :param pipe:
    :param num_images: number of images to generate
    :param num_inference_steps:
    :param image_guidance_scale:
    :param prompt_guidance_scale:
    :return:
    """
    logger.info(f"Generating Pix2Pix image from image using prompt {prompt}")

    result = pipe(
        prompt, image=image, num_inference_steps=num_inference_steps,
        image_guidance_scale=image_guidance_scale,
        guidance_scale=prompt_guidance_scale,
        num_images_per_prompt=num_images
    )

    return result.images


def generate_image(prompt: str, pipe: StableDiffusionPipeline):
    logger.info(f"Generating image from prompt {prompt}")
    # Generate a 512x512 image from a prompt
    # image = pipe(prompt, return_tensors="pt", output_size=512)

    # prompt = "a photo of an astronaut riding a horse on mars"

    # First-time "warmup" pass (see explanation above)
    _ = pipe(prompt, num_inference_steps=1)

    # Results match those from the CPU device after the warmup pass.
    image = pipe(prompt).images[0]
    return image


# def generate_random_image(pipe):
#     source_image = download_image(
#         "https://raw.githubusercontent.com/timothybrooks/instruct-pix2pix/main/imgs/example.jpg")
#     source_prompt = "make it wild"
#
#     result = generate_img2img(source_prompt, source_image, pipe)
#
#     return result


pattern = re.compile(r"(?s)Prompt success rate: #\w+\s+Вероятность успеха: .+@ChangeAiBot\s*")


def remove_prompt_success_rate(message):
    return pattern.sub("", message).strip()
