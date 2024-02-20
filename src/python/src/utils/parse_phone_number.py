import re


class ParsePhoneNumber:
    @staticmethod
    def clean_phone_number(phone_number):
        digits = re.sub(r'\D', '', phone_number)
        return int(digits)
