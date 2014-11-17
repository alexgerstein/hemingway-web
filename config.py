from string import punctuation

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

THESAURI_FOLDER = "thesauri"

WORD = "\w+[\'-]?\w*"
PRICE = "\$[\d.]+"
PUNCTUATION_EXCEPT_HYPHEN = '[' + punctuation.replace('-', '') + "\n" + ']'