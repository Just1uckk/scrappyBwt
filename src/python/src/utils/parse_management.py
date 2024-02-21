import json


class ParseManagement:
    @staticmethod
    def parse_management(response):
        summary = response.xpath(
            '//dt[contains(text(),"Business Management")]/following-sibling::dd[1]/ul/li/span/text()').getall()
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
                else:
                    print("Invalid contact information")
            business_management = json.dumps(result)
            return business_management
        else:
            return None
