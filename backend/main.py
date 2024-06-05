from fastapi import FastAPI, File
from starlette.responses import Response
import io
from segmentation import get_segmentator, get_segments
import logging

logging.basicConfig(level=logging.INFO)
model = get_segmentator()

app = FastAPI(title="DeepLabV3 image segmentation",
              description='Obtain semantic segmentation maps of the image in input via DeepLabV3 implemented in PyTorch.',
              version="0.1.0")


@app.post("/segmentation")
def get_segmentation_map(file: bytes = File(...)):
    '''Get segmentation maps from image file'''
    try:
        segmented_image = get_segments(model, file)
        bytes_io = io.BytesIO()
        segmented_image.save(bytes_io, format='PNG')
        logging.info("Segmentation map created successfully.")
        return Response(bytes_io.getvalue(), media_type="image/png")
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return Response(content=f"Error processing image: {e}", media_type="text/plain")
