from geopy import Nominatim
from geopy.exc import GeocoderUnavailable


def get_country(city):
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        if location:
            return location.address.split(",")[-1].strip()
        else:
            return None
    except GeocoderUnavailable as e:
        print("GEOPY. Geocoding service is unavailable:", e)
        return None
    except Exception as e:
        print("GEOPY. An error occurred:", e)
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
                # "country": get_country(city),
                "country": "Canada",
                "region": region,
                "city": city,
                "street": street,
                "postal_code": postal_code
            }
        else:
            return None
