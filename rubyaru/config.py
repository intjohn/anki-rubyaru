from aqt import mw

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        cfg = mw.addonManager.getConfig(__name__)

        source_fields = cfg["source_fields"]

        if isinstance(source_fields, str):
            source_fields = source_fields.split(",")
        elif isinstance(source_fields, list):
            source_fields = filter(lambda x: isinstance(x, str), source_fields)
        else:
            source_fields = []

        destination_field = cfg["destination_field"]

        if not isinstance(destination_field, str):
            destination_field = None

        self.source_fields = source_fields
        self.destination_field = destination_field

config = Config()
