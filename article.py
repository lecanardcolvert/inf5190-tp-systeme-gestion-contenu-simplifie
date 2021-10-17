import datetime
import re

def is_between_length(value, min, max):
    if min <= len(value) <= max:
        return True
    else:
        return False

def is_valid_identifier_format(value):
    expression = "^[a-zA-Z0-9-._~]+$"
    if re.match(expression, value):
        return True
    else:
        return False

def is_valid_date_format(value):
    try:
        datetime.datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False

class Article:
    def __init__(self):
        pass

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not is_between_length(value, 1, 100):
            raise Exception("Le titre doit être d'une longueur de 1 à 100 "
                            "caractères.")
        self._title = value

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        if not is_between_length(value, 1, 50):
            raise Exception("L'identifiant doit être d'une longueur de 1 à 50 "
                            "caractères.")
        if not is_valid_identifier_format(value):
            raise Exception("L'identifiant peut seulement contenir des "
                            "lettres, chiffres, et quelques symboles (- . _ "
                            "~).")
        self._identifier = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not is_between_length(value, 1, 500):
            raise Exception("L'auteur doit être d'une longueur de 1 à 100 "
                            "caractères.")
        self._author = value

    @property
    def publication_date(self):
        return self._publication_date

    @publication_date.setter
    def publication_date(self, value):
        if not is_valid_date_format(value):
            raise Exception("La date doit être au format AAAA-MM-JJ.")
        self._publication_date = value

    @property
    def paragraph(self):
        return self._paragraph

    @paragraph.setter
    def paragraph(self, value):
        if not is_between_length(value, 1, 500):
            raise Exception("Le paragraphe doit être composé de 1 à 500 "
                            "caractères.")
        self._paragraph = value