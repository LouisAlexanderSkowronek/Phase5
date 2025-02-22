class Voc:
    def __init__(self, native: str, greek: str) -> None:
        self.native = native
        self.greek = greek

    def __eq__(self, other) -> bool:
        return self.native == other.native and self.greek == other.greek
    
    def __str__(self) -> str:
        return f'{self.native},{self.greek}'