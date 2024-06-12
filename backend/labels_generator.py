import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import numpy as np
import cv2


class LabelsGenerator:
    def __init__(self, model_path):
        self.model = load_model(model_path)
        self.label_to_index = {'apple': 0, 'bed': 1, 'bench': 2, 'book': 3, 'bottle': 4, 'bowl': 5,
                               'building-other-merged': 6,
                               'cabinet-merged': 7, 'ceiling-merged': 8, 'chair': 9, 'clock': 10, 'couch': 11,
                               'cup': 12,
                               'curtain': 13, 'dining table': 14, 'dirt-merged': 15, 'donut': 16, 'door-stuff': 17,
                               'fence-merged': 18, 'floor-other-merged': 19, 'floor-wood': 20, 'flower': 21, 'fork': 22,
                               'grass-merged': 23, 'gravel': 24, 'handbag': 25, 'house': 26, 'keyboard': 27,
                               'knife': 28,
                               'laptop': 29, 'light': 30, 'mirror-stuff': 31, 'mountain-merged': 32, 'mouse': 33,
                               'orange': 34,
                               'pavement-merged': 35, 'person': 36, 'pillow': 37, 'potted plant': 38, 'rock-merged': 39,
                               'roof': 40,
                               'rug-merged': 41, 'sea': 42, 'shelf': 43, 'skateboard': 44, 'sky-other-merged': 45,
                               'spoon': 46,
                               'stairs': 47, 'table-merged': 48, 'towel': 49, 'tree-merged': 50, 'tv': 51,
                               'umbrella': 52,
                               'vase': 53, 'wall-brick': 54, 'wall-other-merged': 55, 'wall-stone': 56, 'wall-wood': 57,
                               'water-other': 58, 'window-blind': 59, 'window-other': 60, 'wine glass': 61}

    @staticmethod
    def _preprocess_image(img):
        img = cv2.resize(img, (128, 128))
        img = np.reshape(img, [1, 128, 128, 3])
        return img

    def predict_labels(self, img, max_labels=2):
        img = self._preprocess_image(img)
        prediction = self.model.predict(img)
        labels = []
        for i in range(len(prediction[0])):
            labels.append(
                (list(self.label_to_index.keys())[list(self.label_to_index.values()).index(i)], prediction[0][i]))
        labels.sort(key=lambda x: x[1], reverse=True)
        labels = [label[0] for label in labels[:max_labels]]
        return labels

    def get_labels_by_threshold(self, img, threshold=0.5):
        img = self._preprocess_image(img)
        prediction = self.model.predict(img)
        labels = []
        for i in range(len(prediction[0])):
            if prediction[0][i] > threshold:
                labels.append(list(self.label_to_index.keys())[list(self.label_to_index.values()).index(i)])
        return labels


if __name__ == '__main__':
    # example of usage
    labels_generator = LabelsGenerator('background_label_predictor.h5')
    img = cv2.imread('../dataset/example/image_test.png')
    print(labels_generator.predict_labels(img))
    print(labels_generator.get_labels_by_threshold(img))
