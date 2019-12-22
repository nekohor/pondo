import toml


class Registry:

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls.build_config()
        return cls._instance

    @classmethod
    def build_config(cls):
        configs = {}

        configs["factors"] = toml.load("config/factors_qms.toml")

        return configs
