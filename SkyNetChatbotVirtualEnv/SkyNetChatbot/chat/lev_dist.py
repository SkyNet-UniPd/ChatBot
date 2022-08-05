from Levenshtein import distance


def lev_dist(words: list, correct_words: list) -> bool:
    for word in words:
        for correctWord in correct_words:
            if distance(word.lower(), correctWord.lower()) <= 2:
                return True
    return False


def lev_dist_custom_dist(words: list, correct_words: list, dist: int) -> bool:
    for word in words:
        for correctWord in correct_words:
            if distance(word.lower(), correctWord.lower()) <= dist:
                return True
    return False


def lev_dist_str(words: list, correct_words: list) -> str:
    best_match = 2
    best_word = None

    for word in words:
        for correctWord in correct_words:
            if distance(word.lower(), correctWord.lower()) <= best_match:
                best_match = distance(word.lower(), correctWord.lower())
                best_word = word

    return best_word


def lev_dist_str_correct_w(words: list, correct_words: list) -> str:
    best_match = 2
    best_word = None

    for word in words:
        for correctWord in correct_words:
            if distance(word.lower(), correctWord.lower()) <= best_match:
                best_match = distance(word.lower(), correctWord.lower())
                best_word = correctWord

    return best_word
