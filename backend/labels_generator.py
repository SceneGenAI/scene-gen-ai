import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import numpy as np
import cv2


class LabelsGenerator:
    # real labels:
    # label_to_index = {'apple': 0, 'bed': 1, 'bench': 2, 'book': 3, 'bottle': 4, 'bowl': 5, 'building-other-merged': 6,
    #                   'cabinet-merged': 7, 'ceiling-merged': 8, 'chair': 9, 'clock': 10, 'couch': 11, 'cup': 12,
    #                   'curtain': 13, 'dining table': 14, 'dirt-merged': 15, 'donut': 16, 'door-stuff': 17,
    #                   'fence-merged': 18, 'floor-other-merged': 19, 'floor-wood': 20, 'flower': 21, 'fork': 22,
    #                   'grass-merged': 23, 'gravel': 24, 'handbag': 25, 'house': 26, 'keyboard': 27, 'knife': 28,
    #                   'laptop': 29, 'light': 30, 'mirror-stuff': 31, 'mountain-merged': 32, 'mouse': 33, 'orange': 34,
    #                   'pavement-merged': 35, 'person': 36, 'pillow': 37, 'potted plant': 38, 'rock-merged': 39,
    #                   'roof': 40,
    #                   'rug-merged': 41, 'sea': 42, 'shelf': 43, 'skateboard': 44, 'sky-other-merged': 45, 'spoon': 46,
    #                   'stairs': 47, 'table-merged': 48, 'towel': 49, 'tree-merged': 50, 'tv': 51, 'umbrella': 52,
    #                   'vase': 53, 'wall-brick': 54, 'wall-other-merged': 55, 'wall-stone': 56, 'wall-wood': 57,
    #                   'water-other': 58, 'window-blind': 59, 'window-other': 60, 'wine glass': 61}
    def __init__(self, model_path):
        self.model = load_model(model_path)
        self.label_to_index = {'apple on the table': 0, 'bed in the corner': 1, 'bench': 2, 'book on the table': 3,
                               'bottle on the table': 4, 'bowl on the table': 5, 'building in the background': 6,
                               'cabinet by the wall': 7, 'ceiling in the background': 8, 'chair across the table': 9,
                               'clock on the wall': 10, 'couch': 11, 'cup on the table': 12,
                               'curtain in the background': 13, 'dining table': 14, 'dirt on the ground': 15,
                               'donut on the table': 16, 'door in the background': 17, 'fence in the background': 18,
                               'floor on the ground': 19, 'wooden floor': 20, 'flowers on the ground': 21,
                               'fork on the table': 22, 'grass on the ground': 23, 'gravel on the ground': 24,
                               'handbag': 25, 'house in the background': 26, 'keyboard on the table': 27,
                               'knife on the table': 28, 'laptop on the table': 29, 'sufficient lighting': 30,
                               'mirror in the background': 31, 'mountain in the background': 32,
                               'mouse on the table': 33, 'orange on the table': 34, 'concrete floor': 35,
                               'person sits': 36, 'pillow': 37, 'potted plant in the background': 38,
                               'rock on the ground': 39, 'roof in the background': 40, 'rug on the floor': 41,
                               'sea in the background': 42, 'shelf on the wall': 43, 'skateboard on the floor': 44,
                               'sky above': 45, 'spoon on the table': 46, 'stairs in the background': 47, 'table': 48,
                               'towel hanging': 49, 'tree in the background': 50, 'TV': 51, 'street umbrella': 52,
                               'vase on the table': 53, 'brick wall in the background': 54,
                               'wall in the background': 55, 'stone wall in the background': 56,
                               'wooden wall in the background': 57, 'water in the background': 58,
                               'blind window in the background': 59, 'window in the background': 60,
                               'glass of wine on the table': 61}

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
