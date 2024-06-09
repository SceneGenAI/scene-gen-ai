import os

import requests

service_account_id = os.environ.get('SERVICE_ACC_ID')
key = os.environ.get('API_KEY')
private_key = os.environ.get('API_SECRET')


def data_init():
    data = {}
    data['modelUri'] = 'gpt://b1ga68j4036qlm4nu1rh/yandexgpt/latest'

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
            Всегда генерируй 3 варианта промпта, в ответе должны быть только пронумерованные промпты, без вступления. \
            Пример: \"Батарея в гостинной с голубыми стенами.\" \
            В запросе подается объект. Нужно дописать фон и предлог. Нужно выбирать релевантные фоны для объекта, чтобы картинка, \
            которая могла бы описываться подобным фоном, могла быть на маркетплейсе, продающем мебель. \
            Еще примеры промпта: \
            \"Садовые качели на дворике у загородного дома\", \
            \"Лампа на белом потолке в гостинной с диваном\"."
        },
        {
            "role": "user",
            "text": "Садовые качели"
        }

    ]
    return data


class PromptGenerator:
    """
    Generating a prompt with background for a given object text description.
    Based on YandexGPT model.
    """

    def __init__(self):
        self.service_account_id = os.environ.get('SERVICE_ACC_ID')
        self.key = os.environ.get('API_KEY')
        self.private_key = os.environ.get('API_SECRET')

        self.url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
        self.data = data_init()
        print("Prompt generator initialized.")

    def generate_prompt(self, object_text):
        self.data['messages'][1]['text'] = object_text
        r = requests.post(self.url, headers={'Authorization': 'Api-Key ' + private_key}, json=self.data)
        # if response code is 200, return the generated prompt
        if r.status_code == 200:
            r = r.json()
            return r['result']['alternatives'][0]['message']['text']
        else:
            return 'Error: ' + str(r.status_code)


# Usage example
if __name__ == '__main__':
    pg = PromptGenerator()
    print(pg.generate_prompt('Садовые качели'))
    print(pg.generate_prompt('Лампа'))
    print(pg.generate_prompt('Стол'))
