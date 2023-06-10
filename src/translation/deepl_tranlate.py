from src.api_keys.api_keys import DEEPL_API_KEY
import requests


# languages = ["ES", "PT", "FR", "DE", "JA", "KO", "RU", "IT", "ZH"]


def deepl_translate(text, language):
    url = "https://api-free.deepl.com/v2/translate"
    target_language = language.upper()

    headers = {
        "Authorization": DEEPL_API_KEY
    }

    data = {
        "text": [text],
        "source_lang": "EN",
        "target_lang": target_language,
        "formality": "prefer_less"
    }

    response = requests.post(url=url, headers=headers, data=data)
    data = response.json()

    translated_text = data["translations"][0]["text"]
    return translated_text
