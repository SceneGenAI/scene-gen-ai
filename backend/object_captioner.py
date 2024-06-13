import io

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


class ObjectCaptioner:
    """
    Generating a caption for a given image.
    Based on Blip model.
    """

    def __init__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda")
        print("Object captioning model loaded successfully.")

    def generate_caption(self, file):
        image = Image.open(io.BytesIO(file)).convert('RGB')
        text = "description of the main object, without the background"
        inputs = self.processor(images=image, text=text, return_tensors="pt").to("cuda")
        out = self.model.generate(**inputs)
        caption = self.processor.decode(out[0], skip_special_tokens=True)
        caption = " ".join(caption.split()[9:])
        return caption


# Usage example
if __name__ == '__main__':
    oc = ObjectCaptioner()

    with open("images/shtora.jpg", "rb") as f:
        file = f.read()
        caption = oc.generate_caption(file)
        print(caption)
