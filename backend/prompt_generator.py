import os

import requests

from dotenv import load_dotenv

load_dotenv()


class PromptGenerator:
    """
    Generating a prompt with background for a given object text description.
    Based on YandexGPT model.
    """

    def __init__(self):
        self.private_key = os.getenv('API_SECRET')
        self.catalog_id = os.getenv('CATALOG_ID')

        self.url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
        self.data = self._data_init()
        print("Prompt generator initialized.")

    def generate(self, object_text, additional_objects):
        self.data = self._data_init(object_text, additional_objects)
        r = requests.post(self.url, headers={'Authorization': 'Api-Key ' + self.private_key}, json=self.data)

        if r.status_code == 200:
            r = r.json()
            return r['result']['alternatives'][0]['message']['text']
        else:
            return 'Error: ' + str(r.status_code)

    # @staticmethod
    def _data_init(self, object_text='', additional_objects=None):
        if additional_objects is None:
            additional_objects = []
        data = {}
        data['modelUri'] = f'gpt://{self.catalog_id}/yandexgpt/latest'

        # Additional parameters for the model
        data['completionOptions'] = {
            'stream': False,  # return all completions at once
            'temperature': 0.3,  # the higher the temperature, the more random the completions
            'max_tokens': 1000,  # the maximum number of tokens to generate
        }

        # TODO: 1 - Как прикреплять объекты к фону (трубы для батареи, крепления для качелей, подставки для ламп)
        # TODO 3 - Как подбирать положение и размер объекта на пустой канве
        # TODO: 2 - Промпты для стилей

        # context for the model
        data['messages'] = [
            {
                "role": "system",
                "text": "Нужно сгенерировать промпт формата \"Объект на фоне\" на английском языке. \
                Всегда генерируй 3 варианта промпта, в ответе должны быть только пронумерованные промпты, вступление "
                        "нельзя включать. \
                Ответ формата: \n \
                        1. Промпт \n \
                        2. Промпт \n \
                        3. Промпт \n \
                Пример: \"Батарея в гостинной с голубыми стенами.\" \
                В запросе подается объект и дополнительные объекты, которые желательно добавить в промпт.  Если главный "
                        "объект может быть отнесен к категории \"Садовая мебель\" или \"Освещение\", то использовать "
                        "дополнительные объекты в первом промпте. \n \
                Если главный объект относится к другой категории мебели, например, \"Обогрев\" или \"Сантехника\", то "
                        "другие объекты ИГНОРИРОВАТЬ. Промпт для таких объектов генерируется с нуля БЕЗ дополнительных "
                        "объектов. \n \
                Нужно дописать фон и предлог. Нужно выбирать релевантные фоны для объекта, чтобы картинка,  которая "
                        "могла бы описываться подобным фоном, могла быть на маркетплейсе, продающем мебель. \n \
                        Еще примеры промпта: \
                \"Садовые качели на дворике у загородного дома\", \
                \"Лампа на белом потолке в гостинной с диваном\"."
            },
            {
                "role": "user",
                "text": f"Главный объект: {object_text}. Дополнительные объекты: {', '.join(additional_objects)}."
             }
        ]
        return data


# Usage example
if __name__ == '__main__':
    pg = PromptGenerator()
    # print(pg.generate('Садовые качели, садовая мебель'))
    # print(pg.generate('Лампа, освещение'))
    print(pg.generate('Стол', ['chair across the table', 'curtain in the background']))
