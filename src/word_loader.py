def fetch_words():
    words = []
    file = open("words.txt", "r")
    for word in file:
        words.append(word[:-1])
    words = [w.upper() for w in words]
    file.close()
    return words


def fetch_additional_words():
    from additional_words import additional_words
    return [w.upper() for w in additional_words]
