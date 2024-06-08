from fastapi import FastAPI, File
from starlette.responses import Response
import io
import logging

from generation import get_generator, get_generated_picture

logging.basicConfig(level=logging.INFO)

# Load the diffusion model pipeline
pipeline = get_generator()

app = FastAPI(title="Image Generation with Diffusion Model",
              description='Generate images using a pretrained diffusion model.',
              version="0.1.0")


@app.post("/background-generation")
def generate_image(file: bytes = File(...)):
    try:
        generated_image = get_generated_picture(pipeline, file)
        bytes_io = io.BytesIO()
        generated_image.save(bytes_io, format='PNG')
        logging.info("Image generated successfully.")
        return Response(bytes_io.getvalue(), media_type="image/png")
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return Response(content=f"Error processing image: {e}", media_type="text/plain")
