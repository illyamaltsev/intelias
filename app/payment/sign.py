import logging
from _sha256 import sha256

logger = logging.getLogger("app")


class SignGenerator:
    __sorted_keys_cache = dict()

    def __init__(self, data: dict, secret_key: str):
        self.data = data
        self.secret_key = secret_key

    def generate(self):
        keys_hash = hash(frozenset(self.data))

        try:
            sorted_keys = self.__sorted_keys_cache[keys_hash]
        except KeyError:
            sorted_keys = sorted(self.data)
            self.__sorted_keys_cache[keys_hash] = sorted_keys

        values = [str(self.data[key]) for key in sorted_keys]
        sign_string = ":".join(values) + self.secret_key

        logger.debug(f'Sign string created: "{sign_string}"')
        sign = sha256(sign_string.encode("utf-8")).hexdigest()
        logger.info(f'Sign created: "{sign}"')

        return sign
