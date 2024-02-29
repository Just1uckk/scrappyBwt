class ParseCategories:
    @staticmethod
    def parse_categories(response):
        categories_array = response.xpath('//li//a[contains(@class,"dtm-category")]/text()').getall()
        if len(categories_array) != 0:
            if len(categories_array) == 1:
                return categories_array[0]
            else:
                separator = ' | '
                result_string = separator.join(categories_array)
                return result_string
        else:
            return None
