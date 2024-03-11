import re


class ParseID:
    @staticmethod
    def parse_id(url):
        url_parts = url.split('/')
        slug = url_parts[-1]
        if '#' in slug or '?' in slug:
            if '#' in slug:
                slug = slug.split('#')[0]
            if '?' in slug:
                slug = slug.split('?')[0]
            return slug
        else:
            return slug
