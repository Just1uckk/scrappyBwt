import base64
import hashlib


class GeneratorUniqueId:
    @staticmethod
    def string_to_unique_id(input_string):
        byte_string = input_string.encode('utf-8')
        base64_bytes = base64.b64encode(byte_string)
        unique_id = base64_bytes.decode('utf-8').replace('/', '').replace('+', '').replace('=', '')
        return unique_id

    @staticmethod
    def unique_id_to_string(unique_id):
        padded_unique_id = unique_id.ljust((len(unique_id) + 3) // 4 * 4, '=')
        decoded_bytes = base64.b64decode(padded_unique_id.encode('utf-8'))
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
