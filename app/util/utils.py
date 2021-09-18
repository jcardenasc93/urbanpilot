""" General utils tools """


class DictUtils:
    """Class defined to make operations over dict types"""

    @classmethod
    def search_key(cls, key, element):
        """This methods looks for a key in the nested_dict"""
        if isinstance(element, dict):
            for k, v in element.items():
                if k == key:
                    return v
                elif isinstance(v, dict):
                    cls.search_key(key, v)
                elif isinstance(v, list):
                    cls.search_key(key, v)
        elif isinstance(element, list):
            for obj in element:
                v = cls.search_key(key, obj)
                if v:
                    return v
