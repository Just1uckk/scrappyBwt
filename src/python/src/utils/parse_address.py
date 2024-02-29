import csv
import os

import pycountry


def find_country_by_city(city_name):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'cities15000.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row[1] == city_name:
                country_code = row[8]
                country = pycountry.countries.get(alpha_2=country_code)
                if country:
                    return country.name
    return None


class ParseAddress:
    @staticmethod
    def parse_address(address):
        refactor_address = [item for item in address if item.strip() != "" and item.strip() != ","]
        if len(refactor_address) > 0:
            revert_address_arr = refactor_address[::-1]
            postal_code = revert_address_arr[0]
            region = revert_address_arr[1]
            city = revert_address_arr[2]
            street = None
            if len(revert_address_arr) == 4:
                street = revert_address_arr[3]
            return {
                "full_address": ', '.join(refactor_address),
                "country": find_country_by_city(city),
                "region": region,
                "city": city,
                "street": street,
                "postal_code": postal_code
            }
        else:
            return None
