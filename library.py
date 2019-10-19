import base64
import hashlib


class HackerLibrary:
    @staticmethod
    def encode_base64(string):
        e = string.encode("UTF-8")
        b = base64.b64encode(e)
        s = b.decode("UTF-8")

        return s

    @staticmethod
    def encode_sha256(string):
        sha = hashlib.new('sha256')
        string = string.encode("UTF-8")
        enc_string = hashlib.sha256(string).hexdigest()

        return enc_string
