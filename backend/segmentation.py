import io

import torch
from PIL import Image
from torchvision import transforms
from torchvision.models.segmentation import deeplabv3_resnet50


def get_segmentator():
    model = deeplabv3_resnet50(pretrained=True)
    model.eval()
    return model


def get_segments(model, file):
    input_image = Image.open(io.BytesIO(file)).convert('RGB')
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)

    with torch.no_grad():
        output = model(input_batch)['out'][0]
    output_predictions = output.argmax(0)

    segmented_image = Image.fromarray(output_predictions.byte().cpu().numpy())
    return segmented_image
