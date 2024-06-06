from fastapi import FastAPI, File
from starlette.responses import Response
import io
from diffusers import DiffusionPipeline
import torch
from PIL import Image, ImageOps
from transparent_background import Remover
import logging

logging.basicConfig(level=logging.INFO)

# Load the diffusion model pipeline
model_id = "yahoo-inc/photo-background-generation"
pipeline = DiffusionPipeline.from_pretrained(model_id, custom_pipeline=model_id).to('cuda')

app = FastAPI(title="Image Generation with Diffusion Model",
              description='Generate images using a pretrained diffusion model.',
              version="0.1.0")

def resize_with_padding(img, expected_size):
    img.thumbnail((expected_size[0], expected_size[1]))
    delta_width = expected_size[0] - img.size[0]
    delta_height = expected_size[1] - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
    return ImageOps.expand(img, padding)

@app.post("/generate")
def generate_image(file: bytes = File(...), prompt: str = "A radiator in the living room with grey-blue walls"):
    try:
        img = Image.open(io.BytesIO(file))
        img = resize_with_padding(img, (512, 512))
        remover = Remover()  # default setting
        remover = Remover(mode='base')  # nightly release checkpoint
        fg_mask = remover.process(img, type='map')  # default setting - transparent background
        mask = ImageOps.invert(fg_mask)

        seed = 5
        generator = torch.Generator(device='cuda').manual_seed(seed)
        cond_scale = 1.0
        with torch.autocast("cuda"):
            generated_image = pipeline(
                prompt=prompt, image=img, mask_image=mask, control_image=mask, num_images_per_prompt=1, generator=generator, num_inference_steps=20, guess_mode=False, controlnet_conditioning_scale=cond_scale
            ).images[0]

        bytes_io = io.BytesIO()
        generated_image.save(bytes_io, format='PNG')
        logging.info("Image generated successfully.")
        return Response(bytes_io.getvalue(), media_type="image/png")
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return Response(content=f"Error processing image: {e}", media_type="text/plain")
