import json


class ParseSocialMedia:

    @staticmethod
    def parse_social_media(response):
        media_arr = response.xpath(
            '//dt[contains(text(),"Social Media")]/following-sibling::dd[1]/ul/li/a/@href').getall()
        if len(media_arr) == 0:
            return None
        else:
            data = {}
            for media in media_arr:
                if "instagram" in media:
                    data["instagram"] = media
                if "facebook" in media:
                    data["facebook"] = media
                if "twitter" in media:
                    data["twitter"] = media
            return json.dumps(data)
