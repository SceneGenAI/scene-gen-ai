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
from config import IAM_TOKEN, FOLDER_ID
from labels_generator import LabelsGenerator
from object_captioner import ObjectCaptioner
from prompt_generator import PromptGenerator
from translate import Translator

logging.basicConfig(level=logging.INFO)

# Initialize translation service
translator = Translator(IAM_TOKEN, FOLDER_ID)

# Pre-load needed models
object_captioner = ObjectCaptioner()
prompt_generator = PromptGenerator()
background_generator = BackgroundGenerator()
labels_generator = LabelsGenerator('background_label_predictor.h5')


app = FastAPI(title="Background generation",
              description='Generation pipeline for object background',
              version="0.1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add the origin of your frontend application
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post("/translate")
def translate_text(texts: list[str] = Form(...), source_language: str = Form(...), target_language: str = Form(...)):
    """
    Translate a list of texts
    :param texts: texts to translate
    :param source_language: translate from
    :param target_language: translate to
    :return: translated text as JSONResponse
    """
    try:
        result = translator.translate(texts, source_language, target_language)
        return JSONResponse(content=result)
    except Exception as e:
        logging.error(f"Error translating text: {e}")
        return JSONResponse(content={"error": f"Error translating text: {e}"}, status_code=500)


def prompt_generation(file: bytes = File(...)):
    """
    Generate 3 prompts suggested for the given picture with no background
    :param file: Image file
    :return: JSONResponse with lists of prompts in english and russian.
    """
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
    """
    API endpoint for prompt generation
    :param file: Image file
    :return: prompt for dropdown_options
    """
    contents = await file.read()
    dropdown_options = prompt_generation(contents)
    return dropdown_options


def background_generation(file: bytes, prompt: str):
    """
    Generate background for one object with one prompt
    :param file: Image picture file
    :param prompt: Whole prompt for Stable Diffusion
    :return: an image with background
    """
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
        return base64_image
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return None


@app.post("/background-generation")
async def get_images_endpoint(file: UploadFile = File(...), background: str = Form(...), style: str = Form(...),
                              number_images: int = Form(...)):
    """
    Generate images with different styles
    First image is generated with the given style, the rest are generated with random styles
    :param file: An image file
    :param background: background prompt
    :param style: style label
    :param number_images: number of images to generate at a time
    :return: JSONResponse of array with images
    """

    styles = ['Contemporary', 'Minimalistic', 'Scandinavian', 'Bohemian eclectic', 'Traditional elegance', 'Urban']
    contents = await file.read()
    # make prompt
    if background[-1] == '.':
        background = background[:-1]

    images = []
    if number_images > 1:
        styles.remove(style)
        styles_to_choose = np.random.choice(styles, number_images - 1, replace=False)

    for i in range(number_images):
        if i > 0:
            style = styles_to_choose[i - 1]
        prompt = f"{background}, {style} style."
        print(f"style {i}: {prompt}")
        image = background_generation(contents, prompt)
        if image:
            images.append(image)

    if len(images) == 0:
        return JSONResponse(content={"error": "Error processing image"}, status_code=500)
    return JSONResponse(content={"images": images})


@app.post("/generation-pipeline")
def generation_pipeline(file: bytes = File(...)):
    """
    An automatic pipeline for testing purposes
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
