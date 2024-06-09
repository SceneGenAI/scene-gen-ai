import io
import logging

from fastapi import FastAPI, File
from starlette.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from background_generation import get_generator, get_generated_picture
from object_captioning import ObjectCaptioning
from prompt_generation import PromptGenerator

logging.basicConfig(level=logging.INFO)

# Load the diffusion model pipeline and prompt generator
oc = ObjectCaptioning()
pg = PromptGenerator()
pipeline = get_generator()

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


# @app.post("/prompt-generation")
# def prompt_generation(file: bytes = File(...)):
#     try:
#         caption = oc.generate_caption(file)
#         logging.info("Caption generated successfully.")
#         # return Response(content=caption, media_type="text/plain")
#     except Exception as e:
#         logging.error(f"Error generating caption: {e}")
#         return Response(content=f"Error generating caption: {e}", media_type="text/plain")
#     try:
#         prompt = pg.generate_prompt(caption)
#         logging.info("Prompt generated successfully.")
#         return JSONResponse(content={"prompts": prompt.split('\n')})
#     except Exception as e:
#         logging.error(f"Error generating prompt: {e}")
#         return JSONResponse(content={"error": f"Error generating prompt: {e}"}, status_code=500)


@app.post("/prompt-generation")
def prompt_generation(file: bytes = File(...)):
    try:
        caption = oc.generate_caption(file)
        logging.info("Caption generated successfully.")
    except Exception as e:
        logging.error(f"Error generating caption: {e}")
        return JSONResponse(content={"error": f"Error generating caption: {e}"}, status_code=500)

    try:
        prompt = pg.generate_prompt(caption)
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
        generated_image = get_generated_picture(pipeline, file, prompt)
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
        object_text = oc.generate_caption(file)
        # english prompt
        print("-----------------")
        print(object_text)
    except Exception as e:
        logging.error(f"Error generating caption: {e}")
        return Response(content=f"Error generating caption: {e}", media_type="text/plain")

    try:
        prompt = pg.generate_prompt(object_text)
        # take the first prompt
        print("-----------------")
        print(prompt)
        prompt = prompt.split('\n')[0].split('. ')[1]
        print(prompt)
    except Exception as e:
        logging.error(f"Error generating prompt: {e}")
        return Response(content=f"Error generating prompt: {e}", media_type="text/plain")

    try:
        generated_image = get_generated_picture(pipeline, file, prompt)
        bytes_io = io.BytesIO()
        generated_image.save(bytes_io, format='PNG')
        logging.info("Image generated successfully.")
        return Response(bytes_io.getvalue(), media_type="image/png")
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return Response(content=f"Error processing image: {e}", media_type="text/plain")
