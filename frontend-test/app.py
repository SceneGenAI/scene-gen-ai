import streamlit as st
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from PIL import Image
import io

st.title('DeepLabV3 image segmentation')

# FastAPI endpoint
# url = 'http://fastapi:8000'
url = 'http://backend:8000'
endpoint = '/segmentation'

st.write('''Obtain semantic segmentation maps of the image in input via DeepLabV3 implemented in PyTorch.
         This frontend-test example uses a FastAPI service as backend.
         Visit this URL at `:8000/docs` for FastAPI documentation.''')

image = st.file_uploader('Insert image')


def process(image, server_url: str):
    m = MultipartEncoder(fields={'file': ('filename', image, 'image/jpeg')})
    r = requests.post(server_url, data=m, headers={'Content-Type': m.content_type}, timeout=8000)
    return r


if st.button('Get segmentation map'):
    if image is None:
        st.write("Insert an image!")
    else:
        segments = process(image, url + endpoint)

        # Debugging: Print out the response details
        st.write(f"Response status code: {segments.status_code}")
        st.write(f"Response headers: {segments.headers}")

        try:
            segmented_image = Image.open(io.BytesIO(segments.content)).convert('RGB')
            st.image([image, segmented_image], width=300)
        except Exception as e:
            st.write(f"Error: {e}")
            st.write("Response content is not a valid image.")
            st.write(segments.content)  # Print the response content for debugging
