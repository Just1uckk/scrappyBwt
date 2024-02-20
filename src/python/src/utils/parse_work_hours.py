import json


class ParseWorkHours:
    @staticmethod
    def parse_work_hours(response):
        summary = response.css('summary.dtm-hours')
        if len(summary) > 0:
            days = response.css('div.disclosed-content table tbody tr')
            data = {}
            for day in days:
                day_name = day.xpath('.//th//text()').get().strip()
                hours = day.xpath('.//td//text()').get().strip()
                data[day_name] = hours
            business_json_hours = json.dumps(data)
            return business_json_hours
        else:
            return None
