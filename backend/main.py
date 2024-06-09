import io
import logging

from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response, JSONResponse

from background_generator import BackgroundGenerator
from object_captioner import ObjectCaptioner
from prompt_generator import PromptGenerator

logging.basicConfig(level=logging.INFO)

# Load the diffusion model pipeline and prompt generator
object_captioner = ObjectCaptioner()
prompt_generator = PromptGenerator()
background_generator = BackgroundGenerator()

app = FastAPI(title="Image Generation with Diffusion Model",
              description='Generate images using a pretrained diffusion model.',
              version="0.1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add the origin of your frontend application
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post("/prompt-generation")
def prompt_generation(file: bytes = File(...)):
    try:
        caption = object_captioner.generate_caption(file)
        logging.info("Caption generated successfully.")
        logging.info(caption)
    except Exception as e:
        logging.error(f"Error generating caption: {e}")
        return JSONResponse(content={"error": f"Error generating caption: {e}"}, status_code=500)

    try:
        prompt = prompt_generator.generate(caption)
        logging.info("Prompt generated successfully.")
        prompts = [{"value": idx, "label": prompt_line} for idx, prompt_line in enumerate(prompt.split('\n'))]
        return JSONResponse(content=prompts)
    except Exception as e:
        logging.error(f"Error generating prompt: {e}")
        return JSONResponse(content={"error": f"Error generating prompt: {e}"}, status_code=500)


@app.post("/background-generation")
def background_generation(file: bytes = File(...), prompt: str = ""):
    try:
        if not prompt:
            prompt = 'An object in the living room with grey-blue walls'
        # generated_image = BackgroundGenerator.get_generated_picture(pipeline, file, prompt)
        generated_image = background_generator.get_generated_picture(file, prompt)
        bytes_io = io.BytesIO()
        generated_image.save(bytes_io, format='PNG')
        logging.info("Image generated successfully.")
        return Response(bytes_io.getvalue(), media_type="image/png")
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return JSONResponse(content={"error": f"Error processing image: {e}"}, status_code=500)


@app.post("/generation-pipeline")
def generation_pipeline(file: bytes = File(...)):
    """
    Accept a picture
    1. Get a text description of the object
    2. Generate a text prompt
    3. Diffusion to get a picture with background
    :param file: image file
    :return: image with background
    """
    try:
        object_text = object_captioner.generate_caption(file)
        # english prompt
        print("-----------------")
        print(object_text)
    except Exception as e:
        logging.error(f"Error generating caption: {e}")
        return Response(content=f"Error generating caption: {e}", media_type="text/plain")

    try:
        prompt = prompt_generator.generate(object_text)
        # take the first prompt
        print("-----------------")
        print(prompt)
        prompt = prompt.split('\n')[0].split('. ')[1]
        print(prompt)
    except Exception as e:
        logging.error(f"Error generating prompt: {e}")
        return Response(content=f"Error generating prompt: {e}", media_type="text/plain")

    try:
        generated_image = background_generator.get_generated_picture(file, prompt)
        bytes_io = io.BytesIO()
        generated_image.save(bytes_io, format='PNG')
        logging.info("Image generated successfully.")
        return Response(bytes_io.getvalue(), media_type="image/png")
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return Response(content=f"Error processing image: {e}", media_type="text/plain")
