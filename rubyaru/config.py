from aqt import mw


class Config:
    _instance = None

    def __new__(cls) -> "Config":
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        cfg = mw.addonManager.getConfig(__name__)

        if cfg is None:
            self.source_fields = []
            self.destination_field = None
            return

        source_fields = cfg.get("source_fields", None)

        if isinstance(source_fields, str):
            source_fields = [x.strip() for x in source_fields.split(",")]
        elif isinstance(source_fields, list):
            source_fields = [x.strip() for x in source_fields if isinstance(x, str)]
        else:
            source_fields = []

        source_fields = [x for x in source_fields if x]

        destination_field = cfg.get("destination_field", None)

        destination_field = (
            destination_field.strip()
            if destination_field and isinstance(destination_field, str)
            else None
        )

        self.source_fields = source_fields
        self.destination_field = destination_field

def get_config() -> Config:
    """
    Returns the config instance.
    """
    return Config()
