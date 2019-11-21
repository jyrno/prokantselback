import estnltk

def text_complexity_evaluation(text) -> float:
    coef = avg_char_count_in_sentence(text)
    response = []
    if coef < 3.0:
        response = [25, "Väga lihtne tekst."]
    if coef >= 3.0 and coef < 5.0:
        response = [50, "Lihtne tekst."]
    if coef >= 5.0 and coef < 8.0:
        response = [75, "Raskesti mõistetav tekst."]
    if coef >= 8.0:
        response = [100, "Äärmiselt raskesti mõistetav tekst."]
    return response

def avg_char_count_in_sentence(text) -> float:
    words = (estnltk.Text(text)).tokenize_words().words
    count_of_words = len(words)
    count_of_chars = 0
    for w in words:
        single_word = str(w["text"])
        if single_word.isalpha():
            count_of_chars_in_word = len(list(single_word))
            count_of_chars += count_of_chars_in_word
    return count_of_chars/count_of_words





