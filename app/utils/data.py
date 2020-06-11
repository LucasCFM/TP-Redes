import json


# https://stackoverflow.com/questions/11624190/python-convert-string-to-byte-array
def json_to_byte(j: dict) -> bytearray:
    str_msg = json.dumps( j )
    print(f'str dict: {str_msg}')
    
    b = bytearray()
    b.extend(map(ord, str_msg))
    
    print(f'b: {b}')
    return b


def byte_to_json(b: bytearray) -> dict:
    return json.loads( b.decode("utf-8") )

