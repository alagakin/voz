def latin_to_cyrillic(text):
    latin_cyrillic_mapping = {
        "a": "а", "b": "б", "c": "ц", "č": "ч", "ć": "ћ", "d": "д", "dž": "џ", "đ": "ђ", "e": "е", "f": "ф", "g": "г",
        "h": "х", "i": "и", "j": "ј", "k": "к", "l": "л", "lj": "љ", "m": "м", "n": "н", "nj": "њ", "o": "о", "p": "п",
        "r": "р", "s": "с", "š": "ш", "t": "т", "u": "у", "v": "в", "z": "з", "ž": "ж",
        "A": "А", "B": "Б", "C": "Ц", "Č": "Ч", "Ć": "Ћ", "D": "Д", "Dž": "Џ", "Ð": "Ђ", "E": "Е", "F": "Ф", "G": "Г",
        "H": "Х", "I": "И", "J": "Ј", "K": "К", "L": "Л", "Lj": "Љ", "M": "М", "N": "Н", "Nj": "Њ", "O": "О", "P": "П",
        "R": "Р", "S": "С", "Š": "Ш", "T": "Т", "U": "У", "V": "В", "Z": "З", "Ž": "Ж",
    }

    cyrillic_text = ""
    i = 0
    while i < len(text):
        if i + 2 <= len(text) and text[i:i + 2] in latin_cyrillic_mapping:
            cyrillic_text += latin_cyrillic_mapping[text[i:i + 2]]
            i += 2
        elif text[i] in latin_cyrillic_mapping:
            cyrillic_text += latin_cyrillic_mapping[text[i]]
            i += 1
        else:
            cyrillic_text += text[i]
            i += 1

    return cyrillic_text


def simplify_latin_serbian(text):
    char_mapping = {
        "č": "c", "ć": "c", "đ": "d", "š": "s", "ž": "z",
        "Č": "C", "Ć": "C", "Ð": "D", "Š": "S", "Ž": "Z"
        # Add more mappings as needed
    }

    simplified_text = ""
    for char in text:
        if char in char_mapping:
            simplified_text += char_mapping[char]
        else:
            simplified_text += char

    return simplified_text
