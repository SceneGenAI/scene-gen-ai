import io

import torch
from PIL import Image, ImageOps
from diffusers import DiffusionPipeline
from transparent_background import Remover


class BackgroundGenerator:
    """
    Generating a background for a given object image.
    Based on Diffusion model.
    """

    def __init__(self):
        self.pipeline = self.get_generator()

    @staticmethod
    def resize_with_padding(img, expected_size):
        img.thumbnail((expected_size[0], expected_size[1]))
        delta_width = expected_size[0] - img.size[0]
        delta_height = expected_size[1] - img.size[1]
        pad_width = delta_width // 2
        pad_height = delta_height // 2
        padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
        return ImageOps.expand(img, padding)

    @staticmethod
    def get_generator():
        print("Loading model...")
        model_id = "yahoo-inc/photo-background-generation"
        pipeline = DiffusionPipeline.from_pretrained(model_id, custom_pipeline=model_id)
        pipeline = pipeline.to('cuda')
        print("Model loaded successfully.")
        return pipeline

    @staticmethod
    def expand_background(image, multiplier):
        # TODO choose the placing
        # get the size of the image
        width, height = image.size
        new_image = Image.new('RGB', (int(width * multiplier), int(height * multiplier)))
        new_image.paste(image, (int((width * multiplier - width) / 2), int((height * multiplier - height) / 2)))
        # paste the original image proportionally to the initial picture
        # new_image.paste(image, )
        return new_image

    def get_generated_picture(self, file, prompt: str):
        use_cuda = torch.cuda.is_available()
        device = torch.device("cuda" if use_cuda else "cpu")
        # device = torch.device("cpu")

        # transparent background
        seed = 0
        img = Image.open(io.BytesIO(file)).convert('RGB')
        img = self.expand_background(img, 1.2)
        img = self.resize_with_padding(img, (512, 512))

        # Load background detection model
        remover = Remover()  # default setting
        remover = Remover(mode='base')  # nightly release checkpoint

        # Get foreground mask
        fg_mask = remover.process(img, type='map')

        # generating the picture background
        mask = ImageOps.invert(fg_mask)
        img = self.resize_with_padding(img, (512, 512))
        generator = (torch.Generator(device='cuda')
                     # .manual_seed(seed)
                     )
        cond_scale = 1.0
        with torch.autocast("cuda"):
            controlnet_image = self.pipeline(
                prompt=prompt, image=img, mask_image=mask, control_image=mask, num_images_per_prompt=1,
                generator=generator,
                num_inference_steps=20, guess_mode=False, controlnet_conditioning_scale=cond_scale
            ).images[0]
        return controlnet_image


if __name__ == '__main__':
    bg = BackgroundGenerator()
    prompt = "A hammock in a cozy garden with blooming flowers."
    # prompt = "A radiator on the floor of the living room with grey-blue walls"
    with open("data/gamak.png", "rb") as f:
        file = f.read()
        generated_image = bg.get_generated_picture(file, prompt)
        generated_image.save("generated_image.png")
        print("Image generated successfully.")
