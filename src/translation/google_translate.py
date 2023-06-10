from deep_translator import GoogleTranslator, MyMemoryTranslator


languages = ["es", "pt", "fr", "de", "ja", "ko", "ru", "it", "zh-TW"]


def split_long_text(text):
    if len(text) <= 500:
        return text

    split_text = []
    for i in range(0, len(text), 500):
        split_text.append(text[i:i+500])
    return split_text


def join_back_text(split_text):
    return ''.join(split_text)


def google_translate(text, target_language):
    processed_text = split_long_text(text)

    if isinstance(processed_text, list):
        translated_list = []
        for elem in processed_text:
            translated_elem = GoogleTranslator(source='en', target=target_language).translate(elem)
            translated_list.append(translated_elem)

        translated = join_back_text(translated_list)
    else:
        translated = GoogleTranslator(source='en', target=target_language).translate(processed_text)

    return translated
