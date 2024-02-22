import re


class ParseID:
    @staticmethod
    def parse_id(url):
        pattern = r'\d+'
        id_pattern_result = re.findall(pattern, url)
        business_id = ''.join(id_pattern_result)
        if business_id != '':
            return int(business_id)
        else:
            return None
