import requests

class Translator:
    def __init__(self, iam_token, folder_id):
        self.iam_token = iam_token
        self.folder_id = folder_id
        self.base_url = 'https://translate.api.cloud.yandex.net/translate/v2/translate'

    def translate(self, texts, source_language, target_language):
        body = {
            "sourceLanguageCode": source_language,
            "targetLanguageCode": target_language,
            "texts": texts,
            "folderId": self.folder_id,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.iam_token}"
        }

        response = requests.post(self.base_url, json=body, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
