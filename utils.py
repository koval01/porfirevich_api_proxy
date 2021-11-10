import re, json

from markdownify import markdownify as md


def check_long_words_in_string(string: str) -> bool:
    """
    Проверка наличия слишком довгих слов/елементов в строке
    """
    status = True
    s = string.split()
    for i in s:
        if len(i) > 29:
            status = False

    return status


def cleanhtml(raw_html: str) -> str:
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def fix_string(string: str) -> str:
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


def remove_empty(array: list) -> list:
    return [t for t in array if not re.findall(r"<.></.>", t)]


def decode_story_string(array: list) -> str:
    array = [
        fix_string(
            cleanhtml(el[0])
        ) for el in json.loads(array) if check_long_words_in_string(el[0])
    ]
    
    result = remove_empty(list(map(
        lambda x: "<b>%s</b>" % x[0] if x[1] else "<i>%s</i>" % x[0], array
    )))
            
    return ''.join(list(map(lambda x: md(x), struct_array)))
