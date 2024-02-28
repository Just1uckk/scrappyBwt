import re


class ParsePhoneNumber:
    @staticmethod
    def clean_phone_number(phone_number):
        if phone_number:
            digits = re.sub(r'\D', '', phone_number)
            return int(digits)
        else:
            return None
