from googletrans import Translator

translator = Translator()

def translate_text(text: str, target_lang: str) -> str:
    """Translate text to target language"""
    if target_lang == "en":
        return text
    return translator.translate(text, dest=target_lang).text
