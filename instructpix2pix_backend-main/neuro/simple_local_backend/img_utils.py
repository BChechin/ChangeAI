from PIL import Image, ImageDraw, ImageFont
from PIL.ImageDraw import ImageDraw as IDraw
from pathlib import Path
from textwrap import wrap
from timeout_decorator import timeout
from typing import Union

__all__ = (
    'crop_resize_for_sd',
    'print_result'
)
resources_path = Path(__file__).parent / 'resources'


def rounded_rectangle(self: IDraw, xy, corner_radius, fill=None, outline=None):
    upper_left_point = xy[0]
    bottom_right_point = xy[1]
    self.rectangle(
        [
            (upper_left_point[0], upper_left_point[1] + corner_radius),
            (bottom_right_point[0], bottom_right_point[1] - corner_radius)
        ],
        fill=fill,
        outline=outline
    )
    self.rectangle(
        [
            (upper_left_point[0] + corner_radius, upper_left_point[1]),
            (bottom_right_point[0] - corner_radius, bottom_right_point[1])
        ],
        fill=fill,
        outline=outline
    )
    self.pieslice(
        [upper_left_point, (upper_left_point[0] + corner_radius * 2, upper_left_point[1] + corner_radius * 2)],
        180,
        270,
        fill=fill,
        outline=outline
    )
    self.pieslice(
        [(bottom_right_point[0] - corner_radius * 2, bottom_right_point[1] - corner_radius * 2), bottom_right_point],
        0,
        90,
        fill=fill,
        outline=outline
    )
    self.pieslice([(upper_left_point[0], bottom_right_point[1] - corner_radius * 2),
                   (upper_left_point[0] + corner_radius * 2, bottom_right_point[1])],
                  90,
                  180,
                  fill=fill,
                  outline=outline
                  )
    self.pieslice([(bottom_right_point[0] - corner_radius * 2, upper_left_point[1]),
                   (bottom_right_point[0], upper_left_point[1] + corner_radius * 2)],
                  270,
                  360,
                  fill=fill,
                  outline=outline
                  )


ImageDraw.rounded_rectangle = rounded_rectangle


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


@timeout(10)
def crop_resize_for_sd(pil_img):
    img_width, img_height = pil_img.size
    if img_width < img_height:
        best_img_width = 512
        best_img_height = int(img_height * (512 / img_width))
    else:
        best_img_width = int(img_width * (512 / img_height))
        best_img_height = 512

    result = pil_img.resize((best_img_width, best_img_height))

    if best_img_width > 1024:
        best_img_width = 1024
        result = crop_center(result, 1024, 512)
    if best_img_height > 1024:
        best_img_height = 1024
        result = crop_center(result, 512, 1024)

    return result


def is_text_inside_box(font_path: str, size: int, text: str, width: int, height: int) -> Union[bool, str]:
    font = ImageFont.truetype(font_path, size=size, encoding='UTF-8')
    left_text = text.strip()
    last_line = ""
    result = []
    saved_width = width // size * 2
    decline = False
    result_height = 0

    while left_text != "":
        line = wrap(left_text, width=saved_width)[0]
        if line == last_line:
            if decline:
                saved_width -= 1
            else:
                saved_width += 1
            continue
        else:
            last_line = line
        line_size = font.getsize(line)

        if line_size[0] == width or (line_size[0] < width and (decline or line == left_text)):
            decline = False
            result.append(line)
            left_text = left_text[len(line):].strip()
            result_height += line_size[1]
            if result_height > height:
                result.pop()
                break
        elif line_size[0] < width:
            saved_width += 1
        else:
            saved_width -= 1
            decline = True

    return left_text == "" and result_height <= height, result


def get_text_img_box(font_path: str, text: str, width: int, height: int, color: str) -> Image:
    maxsize = 80
    minsize = 5
    result_text = None

    while maxsize > minsize + 1:
        testsize = (maxsize + minsize) // 2
        possible, textarr = is_text_inside_box(font_path, testsize, text, width, height)

        if possible:
            result_text = '\n'.join(textarr)
            minsize = testsize
        else:
            maxsize = testsize

    if not result_text:
        _, textarr = is_text_inside_box(font_path, minsize, text, width, height)
        result_text = '\n'.join(textarr)

    font = ImageFont.truetype(font_path, size=minsize, encoding='UTF-8')
    result = Image.new("RGBA", (width, height))
    draw_text = ImageDraw.Draw(result)
    draw_text.multiline_text(
        (0, 0),
        result_text,
        font=font,
        fill=color)
    return result


@timeout(10)
def print_result(orig: Image, transformed: Image, prompt: str, prompt_cfg: float, image_cfg: float) -> Image:
    gap = 15
    corner_radius = 15
    desc_gap = 20
    desc_height = 160
    prompt_height = 130
    background_path = str(resources_path / "tgbackground.jpg")
    qr_path = str(resources_path / "tgqr.png")
    font_path = str(resources_path / "itimcyrillic.otf")
    info_text_color = "#8E8E8E"
    prompt_color = "#2F2F2F"

    transformed = transformed.resize(orig.size)

    background = Image.open(background_path).convert("RGBA")
    qr = Image.open(qr_path).convert("RGBA").resize((desc_height, desc_height))

    img_width, img_height = orig.size
    if img_width > img_height:
        result_width = img_width + gap * 2
        result_height = img_height * 2 + gap * 3 + desc_gap + desc_height
        offsets = ((gap, gap), (gap, img_height + gap * 2), (gap, img_height * 2 + gap * 2 + desc_gap))
    else:
        result_width = img_width * 2 + gap * 3
        result_height = img_height + gap * 2 + desc_gap + desc_height
        offsets = ((gap, gap), (img_width + gap * 2, gap), (gap, img_height + gap + desc_gap))

    max_dim = max(result_width, result_height)
    background = background.resize((max_dim, max_dim))
    result = crop_center(background, result_width, result_height)

    mask = Image.new("L", orig.size)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(((0, 0), mask.size), corner_radius, fill="white")

    result.paste(orig, offsets[0], mask)
    result.paste(transformed, offsets[1], mask)

    prompt_width = result_width - gap * 3 - qr.size[0] - 10
    prompt_bg = Image.new("RGB", (prompt_width, prompt_height))
    prompt_bg_mask = Image.new("L", prompt_bg.size)
    draw = ImageDraw.Draw(prompt_bg_mask)
    for i in range(0, 10):
        color = "#" + (str(55 - i * 4) * 3)
        draw.rounded_rectangle(((0, i), prompt_bg_mask.size), corner_radius, fill=color)
    result.paste(prompt_bg, offsets[2], prompt_bg_mask)

    prompt_img = get_text_img_box(font_path, prompt, prompt_width - 10, prompt_height - 10, prompt_color)
    result.alpha_composite(prompt_img, dest=(offsets[2][0] + 10, offsets[2][1] + 10))

    font = ImageFont.truetype(font_path, size=26, encoding='UTF-8')
    draw_text = ImageDraw.Draw(result)
    draw_text.text(
        (gap, offsets[2][1] + prompt_height + 3),
        f"prompt strength: {prompt_cfg}   image strength: {image_cfg}",
        font=font,
        fill=info_text_color)

    result.alpha_composite(qr, dest=(result_width - gap - qr.size[0] - 3, offsets[2][1]))

    return result
