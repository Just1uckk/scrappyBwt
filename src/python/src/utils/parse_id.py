import re


class ParseID:
    @staticmethod
    def parse_id(url):
        pattern = r'\d+'
        id_pattern_result = re.findall(pattern, url)
        business_id = ''.join(id_pattern_result)
        return int(business_id)
