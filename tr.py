import requests

# TODO  Заходим сюда "https://oauth.yandex.ru/verification_code#access_token=y0_AgAAAAAgVAurAATuwQAAAAEHONBcAAAKNSixRqxF-LytCIu05GNPviYm8Q&token_type=bearer&expires_in=31513279&cid=czrmkfkupwk8qbu20xjxxhhxuw"
# TODO копируем код и открываем PowerShell

'''
$yandexPassportOauthToken = "<СЮДА ПИШЕМ КОД>"
$Body = @{ yandexPassportOauthToken = "$yandexPassportOauthToken" } | ConvertTo-Json -Compress
Invoke-RestMethod -Method 'POST' -Uri 'https://iam.api.cloud.yandex.net/iam/v1/tokens' -Body $Body -ContentType 'Application/json' | Select-Object -ExpandProperty iamToken
'''
# TODO получаем IAM_TOKEN и вставляем сюда

IAM_TOKEN = ""
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


