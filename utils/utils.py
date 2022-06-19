import unicodedata

def isLengthOK(min, max, text):
    length = len(text)

    return min <= length <= max

def isAlphaNumeric(text: str):
    return text.isalnum()

def ishalfWidth(text: str):
    for char in text:
        status = unicodedata.east_asian_width(char)
        if status != 'H':
            return False

    return True


def validate_password(password):
    data = {
        "text_type": isAlphaNumeric(password),
        "char_type": ishalfWidth(password),
        "length": isLengthOK(8,20,password),
    }

    return data


def validate_username(username):
    data = {
        "text_type": isAlphaNumeric(username),
        "char_type": ishalfWidth(username),
        "length": isLengthOK(6,20, username),
    }
    return data



