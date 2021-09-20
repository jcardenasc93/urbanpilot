""" A redis helper """
import redis
import json


class RedisHelper:
    def __init__(self, redis_uri: str):
        self.__redis_uri = redis_uri
        self.__connection = redis.from_url(self.__redis_uri)
        self._check_connection()

    def _check_connection(self):
        try:
            self.__connection.ping()
        except Exception as e:
            print(e)

    def get_value(self, key):
        """Returns key value from Redis"""
        if value := self.__connection.get(key):
            return json.loads(value)
        return None

    def get_multiple_values(self, keys: list):
        """Returns multiples keys values as a list"""
        return [self.get_value(key) for key in keys]

    def set_value(self, key, value):
        """Sets value on Redis"""
        if isinstance(value, dict):
            value = json.dumps(value)
        self.__connection.set(key, value)

    def get_or_set(self, key, value):
        """Retrieves key value if exists on Redis or insert the new data"""
        if val := self.get_value(key):
            return val
        self.set_value(key, value)
