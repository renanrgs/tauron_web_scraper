def singleton(class_):
    _instance = {}

    def get_instance(*args, **kwargs):
        if class_ not in _instance:
            _instance[class_] = class_(*args, **kwargs)
        return _instance[class_]

    return get_instance


class Singleton(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]
