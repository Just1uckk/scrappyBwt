import base64

def string_to_unique_id(s):
    byte_string = s.encode('utf-8')
    base64_bytes = base64.b64encode(byte_string)
    unique_id = base64_bytes.decode('utf-8').replace('/', '').replace('+', '').replace('=', '')
    return unique_id

def unique_id_to_string(unique_id):
    padded_unique_id = unique_id.ljust((len(unique_id) + 3) // 4 * 4, '=')
    decoded_bytes = base64.b64decode(padded_unique_id.encode('utf-8'))
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

original_string = "ab/airdrie/profile/water-gardens/fsl-inc-0017-62884"
unique_id = string_to_unique_id(original_string)
print("Уникальный ID:", unique_id)

decoded_string = unique_id_to_string(unique_id)
print("Обратно в строку:", decoded_string)
