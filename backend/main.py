import base64
import io
import logging

import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.responses import Response

from background_generator import BackgroundGenerator
from labels_generator import LabelsGenerator
from object_captioner import ObjectCaptioner
from prompt_generator import PromptGenerator
from translate import Translator
from config import IAM_TOKEN, FOLDER_ID

logging.basicConfig(level=logging.INFO)

# Initialize translation service
translator = Translator(IAM_TOKEN, FOLDER_ID)

# # Load the diffusion model pipeline and prompt generator
object_captioner = ObjectCaptioner()
prompt_generator = PromptGenerator()
background_generator = BackgroundGenerator()
labels_generator = LabelsGenerator('background_label_predictor.h5')
#
app = FastAPI(title="Image Generation with Diffusion Model",
              description='Generate images using a pretrained diffusion model.',
              version="0.1.0")
#
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add the origin of your frontend application
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post("/translate")
def translate_text(texts: list[str], source_language: str, target_language: str):
    """
    Translate a list of texts into the target language
    """
    try:
        result = translator.translate(texts, source_language, target_language)
        return JSONResponse(content=result)
    except Exception as e:
        logging.error(f"Error translating text: {e}")
        return JSONResponse(content={"error": f"Error translating text: {e}"}, status_code=500)


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
        img = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
        labels = labels_generator.predict_labels(img, max_labels=2)
        prompt = prompt_generator.generate(object_text, *labels)
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


def prompt_generation(file: bytes = File(...)):
    try:
        caption = object_captioner.generate_caption(file)
        logging.info("Caption generated successfully.")
        logging.info(caption)
    except Exception as e:
        logging.error(f"Error generating caption: {e}")
        return JSONResponse(content={"error": f"Error generating caption: {e}"}, status_code=500)

    try:
        logging.info("Predicting labels...")
        img = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
        labels = labels_generator.predict_labels(img, max_labels=2)
        logging.info(f"Labels predicted successfully: {labels}")
    except Exception as e:
        logging.error(f"Error predicting labels: {e}")
        return JSONResponse(content={"error": f"Error predicting labels: {e}"}, status_code=500)

    try:
        prompt = prompt_generator.generate(caption, labels)
        logging.info(f"Prompt generated successfully: {prompt}")
        prompts = [{"value": idx, "label": prompt_line} for idx, prompt_line in enumerate(prompt.split('\n'))]
    except Exception as e:
        logging.error(f"Error generating prompt: {e}")
        return JSONResponse(content={"error": f"Error generating prompt: {e}"}, status_code=500)

    try:
        labels = [prompt["label"] for prompt in prompts]
        translated_labels = translator.translate(labels, "en", "ru")
        translated_prompts = [{"value": option["value"], "label": trans_label["text"]} for option, trans_label in
                              zip(prompts, translated_labels["translations"])]
        response = {
            "en": prompts,
            "ru": translated_prompts
        }
        return JSONResponse(content=response)


    except Exception as e:
        logging.error(f"Error translating prompts: {e}")
        return [{"error": f"Error translating prompt: {e}"} for _ in prompts]


@app.post("/prompt-generation")
async def get_dropdown_options_endpoint(file: UploadFile = File(...)):
    contents = await file.read()

    dropdown_options = prompt_generation(contents)

    return dropdown_options


def background_generation(file: bytes, prompt: str):
    print(f"Prompt: {prompt}")
    try:
        if not prompt:
            prompt = 'An object in the living room with grey-blue walls'
        generated_image = background_generator.get_generated_picture(file, prompt)
        bytes_io = io.BytesIO()
        generated_image.save(bytes_io, format='PNG')
        bytes_io.seek(0)  # Reset the pointer to the beginning of the BytesIO object
        base64_image = base64.b64encode(bytes_io.read()).decode('utf-8')
        logging.info("Image generated successfully.")
        return JSONResponse(content={"image": base64_image})
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return JSONResponse(content={"error": f"Error processing image: {e}"}, status_code=500)


@app.post("/background-generation")
async def get_images_endpoint(file: UploadFile = File(...), background: str = Form(...), style: str = Form(...)):
    contents = await file.read()
    # make prompt
    if background[-1] == '.':
        background = background[:-1]
    prompt = f"{background}, {style} style."
    print("style" + prompt)
    image = background_generation(contents, prompt)
    if (background == ""):
        print("empty string")
        print(style)
    else:
        print(background)
    return image


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
