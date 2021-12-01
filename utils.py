import base64


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def encrypt_base64(_password: str) -> str:
        bytes_str = str.encode(_password, encoding='utf-8')
        b64password = base64.b64encode(bytes_str)
        return b64password.decode(encoding='utf-8')
