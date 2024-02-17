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
        start_class = response.css('.dtm-stars')
        if len(start_class) > 0:
            parent_class = start_class.xpath('..')
            next_class = parent_class.xpath('following-sibling::p[1]/text()').get()
            return regular_pattern(next_class)
        else:
            return None
