from googletrans import Translator

translator = Translator()

def translate(text, dest="en"):
    return translator.translate(text, dest=dest).text
