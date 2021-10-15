import re, json

from markdownify import markdownify as md

def check_long_words_in_string(string) -> bool:
    """
    Проверка наличия слишком довгих слов/елементов в строке
    """
    status = True
    s = string.split()
    for i in s:
        if len(i) > 29:
            status = False

    return status


def cleanhtml(raw_html) -> str:
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def fix_string(string) -> str:
    in_word = string
    in_between_words = ['-', '–']
    in_sentences = ['«', '(', '[', '{', '"', '„', '\'']
    string = string.replace("\n\n", "\n")
    for item in in_between_words:
        regex = r'\w[%s]\s\w' % item
        in_word = re.findall(regex, string)

        for x in in_word:
            a = x[:1]; b = x[3:4]
            string = string.replace(x, a + '-' + b)

    for item in in_sentences:
        string = string.replace(f' {item} ', f' {item}')
    return string


def decode_story_string(array) -> str:
    struct_array = []
    array = json.loads(array)
    for i in array:
        text = cleanhtml(i[0])
        text = fix_string(text)
        if check_long_words_in_string(text):
            if i[1]:
                struct_array.append("<b>%s</b>" % text) # Bold
            else:
                struct_array.append("<i>%s</i>" % text) # Italic
        else:
            struct_array.append('<b>Произошла ошибка!</b>')
    struct_array = list(map(lambda x: md(x), struct_array))
    return ''.join(struct_array)
