""" Module with dict object utils """


class DictUtils:
    @classmethod
    def search_nested_keys_value(cls, base_dict: dict, keys: list):
        """This method allows to get values in a nested dict with multiple keys"""
        if not keys:
            return None

        value = base_dict
        for key in keys:
            value = value.get(key)
        return value

    @classmethod
    def search_multiple_keys(cls, base_dict: dict, keys: list):
        """Search multiple keys in a dict"""
        return [base_dict.get(key) for key in keys]
