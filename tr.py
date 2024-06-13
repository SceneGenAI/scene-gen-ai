import requests

IAM_TOKEN = "t1.9euelZqWm8eNmc2PyprHycqcnM6elO3rnpWal8-WkJqMj5iUm5eTl5qWmcvl8_cyZFNM-e82MXw6_N3z93ISUUz57zYxfDr8zef1656Vms6YmsuPnZKZjYyNzZ6Xx8zJ7_zF656Vms6YmsuPnZKZjYyNzZ6Xx8zJ.YzL5ylD3gorQQt98OCc-O37YqYfIa0b8EDni6K74PAMwEhu4A8vQagBbrPwaFFoE3_hofVt_JL6qnJocJakQCg"
folder_id = 'b1g2k660gd43iko0496i'
target_language = 'ru'
texts = ["Hello", "World"]

body = {
    "targetLanguageCode": target_language,
    "texts": texts,
    "folderId": folder_id,
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {0}".format(IAM_TOKEN)
}

response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                         json=body,
                         headers=headers
                         )

print(response.text)


