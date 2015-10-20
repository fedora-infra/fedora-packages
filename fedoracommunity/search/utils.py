import urllib

words_translation = {'d-bus': 'dbus',
                     'gtk+': 'gtk'}

reserved_chars = ['+', '-', '\'', '"']


def filter_search_string (string):
    """Replaces xapian reserved characters with underscore, lowercases
       the string and replaces spelling of certain words/names with more
       common versions

       Reserved Characters:
           +, -, ', "
    """

    string = string.lower()
    for key, value in words_translation.items():
        string = string.replace(key, value)

    for char in reserved_chars:
        string = string.replace(char, '_')

    return string
