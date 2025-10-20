#убрать переносы
def delete_fake_lines(text):
    new_text = ''
    i = 0
    while i < len(text):
        c = text[i]
        if c == '-' and text[i+1] == ' ' and text[i-1] != ' ':
            i += 2
        else:
            new_text += c
            i += 1
    return new_text
    
#добавить пробелы
def split_words(text):
    new_text = ''
    i = 0
    while i < len(text):
        c = text[i]
        if (c.isupper()) and (not text[i-1].isupper()):
            new_text += ' '
        new_text += c
        i += 1
    return new_text

#добавить нехватающие пробелы
def add_spaces(text):
    new_text = ''
    i = 0
    flag = False
    while i < len(text):
        c = text[i]
        if c == '.' and not (i + 1 == len(text))  and not ((text[i+1] != ' ') or (text[i+1] != '\n')):
            flag = True
        new_text += c
        if flag:
            new_text += ' '
        i += 1
    return new_text

def preprocess(text):
    return add_spaces(split_words(delete_fake_lines(text)))