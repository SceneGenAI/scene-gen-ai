from PIL import Image, ImageOps
from diffusers import DiffusionPipeline
from transparent_background import Remover
import torch
import io


def resize_with_padding(img, expected_size):
    img.thumbnail((expected_size[0], expected_size[1]))
    delta_width = expected_size[0] - img.size[0]
    delta_height = expected_size[1] - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
    return ImageOps.expand(img, padding)


def get_generator():
    print("Loading model...")
    model_id = "yahoo-inc/photo-background-generation"
    pipeline = DiffusionPipeline.from_pretrained(model_id, custom_pipeline=model_id)
    # pipeline = pipeline.to('cuda')
    print("Model loaded successfully.")
    return pipeline


def get_generated_picture(pipeline, file):
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    # device = torch.device("cpu")

    # transparent background
    seed = 0
    img = Image.open(io.BytesIO(file)).convert('RGB')
    img = resize_with_padding(img, (512, 512))

    # Load background detection model
    remover = Remover()  # default setting
    remover = Remover(mode='base')  # nightly release checkpoint

    # Get foreground mask
    fg_mask = remover.process(img, type='map')

    # generating the picture background
    mask = ImageOps.invert(fg_mask)
    img = resize_with_padding(img, (512, 512))
    generator = torch.Generator(device='cuda').manual_seed(seed)
    # prompt = 'A dark swan on a beach'
    prompt = 'A radiator in the living room with grey-blue walls'
    cond_scale = 1.0
    with torch.autocast("cuda"):
        controlnet_image = pipeline(
            prompt=prompt, image=img, mask_image=mask, control_image=mask, num_images_per_prompt=1, generator=generator,
            num_inference_steps=20, guess_mode=False, controlnet_conditioning_scale=cond_scale
        ).images[0]
    return controlnet_image
