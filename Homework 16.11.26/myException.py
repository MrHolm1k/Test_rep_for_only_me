class InvalidInput(Exception):
    def __init__(self, massage: str = "Невалидная запись"):
        super().__init__(massage)

