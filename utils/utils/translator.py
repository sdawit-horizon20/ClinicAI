from googletrans import Translator

translator = Translator()

def translate_to_english(text):
    try:
        return translator.translate(text, dest='en').text
    except:
        return text

def translate_from_english(text, target_lang='en'):
    if target_lang == 'en':
        return text
    try:
        return translator.translate(text, dest=target_lang).text
    except:
        return text
