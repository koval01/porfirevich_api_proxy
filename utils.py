import re
import json

from markdownify import markdownify as md


class UtilsMethods:
    @staticmethod
    def check_long_words_in_string(string: str) -> bool:
        """
        Checking for too long words / elements in a string
        :param string: The string you want to check
        :return: Bool result. If success - True or another False
        """
        return not max([True for i in string.split() if len(i) > 29]+[False])

    @staticmethod
    def cleanhtml(raw_html: str) -> str:
        """
        Remove HTML tags from string
        :param raw_html: HTML text string
        :return: Clean string
        """
        return re.sub(r'<.*?>', '', raw_html)

    @staticmethod
    def fix_string(string: str) -> str:
        """
        Fix known issues in the string
        :param string: A string that needs to be checked and corrected
        :return: Fixed string
        """
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
            string = re.sub(r"(\w)\n", r"\1", string)

        return string

    @staticmethod
    def remove_empty(array: list) -> list:
        """
        Detect and remove empty tags, to avoid confusion when converting to Markdown
        :param array: Array to check
        :return: Cleaned array
        """
        return [t for t in array if not re.findall(r"<.></.>", t)]

    @staticmethod
    def check_len_story(array: list) -> bool:
        """
        Check that the record does not exceed the maximum allowable length
        :param array: Content array
        :return: Bool result check. True if successfuly
        """
        return len("".join([el[0] for el in array])) < 800

    @staticmethod
    def decode_story_string(array: list) -> str:
        """
        Decoding content from the format we receive from Porfirevich to Markdown format
        :param array: Porfirevich content array
        :return: Markdown text
        """
        array = [
            [UtilsMethods.fix_string(UtilsMethods.cleanhtml(el[0])), el[1]]
            for el in json.loads(array) if UtilsMethods.check_long_words_in_string(el[0])
        ]
        result = list(map(
            lambda x: "<b>%s</b>" % x[0] if x[1] else "<p>%s</p>" % x[0], array
        ))
        result = UtilsMethods.remove_empty(result)

        return ''.join(list(map(lambda x: md(x), result)))

    @staticmethod
    def create_story_list(array: list) -> list:
        return [{
            "content": UtilsMethods.decode_story_string(el["content"]),
            "createdAt": el["createdAt"].replace("T", " ").replace(".000Z", ""),
            "likesCount": el["likesCount"], "id": el["id"]
        } for el in array if UtilsMethods.check_len_story(el["content"])]
