import json


class ParseContactInformation:
    @staticmethod
    def parse_contact_information(response):
        summary = response.xpath(
            '//dt[contains(text(),"Contact Information")]/following-sibling::dd[1]/ul/li/span/text()').getall()
        if len(summary) > 0:
            result = []
            for item in summary:
                parts = item.split(', ')
                if len(parts) > 2:
                    result.append({"name": parts[0], "position": parts[1]})
                if len(parts) == 2:
                    name, position = parts
                    result.append({"name": name, "position": position})
                elif len(parts) == 1:
                    result.append({"name": parts[0]})
            business_contact_information = json.dumps(result)
            return business_contact_information
        else:
            return None
