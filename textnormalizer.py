import re


class Normalizer:
    """
    perform simple rule based text normalization:
    replace numbers by NUM, smiles to SMILE, lead to lower case and so on
    """

    def __init__(self):
        pass

    def replace_smile(self, line):
        """
        replace sad smiles with SAD_SMILE, fun smile with FUN_SMILE and other smiles with SMILE
        :param line: line with (or without) smiles
        :type line: str
        :return:
        """
        fun_smile_regexp = re.compile("[;:]-?\)+|=\)")
        sad_smile_regexp = re.compile(":-?\(+|=\(")
        other_smiles = re.compile(":-?D|<3|:-?[C0OP]]|:-\*|=3|\[:\|\|\|:\]|O_o")

        line = sad_smile_regexp.sub("SAD_SMILE", line)
        line = other_smiles.sub("EMOTICON", line)
        line = fun_smile_regexp.sub("FUN_SMILE", line)
        return line

    def replace_time(self, line):
        """
        replace time in format hh:mm or hh-mm with TIME
        regexp borrowed from http://stackoverflow.com/questions/7536755/regular-expression-for-matching-hhmm-time-format
        :param line: line with (or without) numbers
        :type line: str
        :return:
        """
        time_regexp = re.compile("([0-9]|0[0-9]|1[0-9]|2[0-3])(:|-)[0-5][0-9]")
        return time_regexp.sub("TIME", line)

    def replace_number(self, line):
        """
        replace number with NUM
        :param line: line with (or without) numbers
        :type line: str
        :return:
        """
        num_regexp = re.compile("[0-9]+\.?[0-9]*")
        return num_regexp.sub("NUM", line)

    def replace_phone_number(self, line):
        """
        replace phone number with PHONE. Phone number may be in format
        8 (nnn) nnn-nn-nn
        or +nnn (nnn) nnn-nn-nn
        and some other
        :param line: line with (or without) numbers
        :type line: str
        :return:
        """
        country_code = "([\+[0-9]+|8])"
        operator_code = "([0-9]{3}|\([0-9]{3}\))"
        sep = "([\s\- ]?)"
        phone = country_code + sep + operator_code + sep + "([0-9]{3})" + sep + "([0-9]{2})" + sep + "([0-9]{2})"
        phone_num_regexp = re.compile(phone)
        return phone_num_regexp.sub("PHONE", line)

    def replace_url(self, line):
        """
        replace url with URL
        :param line: line with urls
        :type line: str
        :return:
        """
        url_regexp = re.compile(
            "https?:\\/\\/(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%_\\+.~#?&//=]*)"
        )
        return url_regexp.sub("URL", line)

    def replace_non_letters(self, line):
        """
        replace all non letters with space
        :param line: string with nonletters
        :type line: str
        :return:
        """
        non_letters = re.compile("\W+")
        return non_letters.sub(" ", line).strip()

    def normalize(self, line):
        for method in [str.lower, self.replace_phone_number, self.replace_time, self.replace_number, self.replace_url,
                       self.replace_smile, self.replace_non_letters]:
            line = method(line)
        return line

