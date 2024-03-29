import base64
import hashlib
import random


class HackerLibrary:
    @staticmethod
    def encode_base64(string):
        e = string.encode("UTF-8")
        b = base64.b64encode(e)
        s = b.decode("UTF-8")

        return s

    @staticmethod
    def decode_base64(string):

        e = string.encode("UTF-8")
        b = base64.b64decode(e)
        s = b.decode("UTF-8")

        return s

    @staticmethod
    def encode_sha256(string):
        string = string.encode("UTF-8")
        enc_string = hashlib.sha256(string).hexdigest()

        return enc_string

    @staticmethod
    def choose_reply(arr, feelings):
        if feelings <= 33:
            return random.choice(arr[0])
        elif feelings <= 66:
            return random.choice(arr[1])
        else:
            return random.choice(arr[2])
