import re


def regular_pattern(text):
    pattern = r'\d+'
    matches = re.findall(pattern, text)
    if matches:
        average_reviews = int(matches[0])
        return average_reviews
    else:
        return None


class ParseCustomerReviews:
    @staticmethod
    def parse_customer_reviews(response):
        tag = response.xpath("//p[contains(text(), 'Average')]//text()").get()
        if tag is None:
            return None
        else:
            return regular_pattern(tag)
