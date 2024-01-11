class res:
    def __init__(self, success: bool, payload: any = None, message: str = None) -> None:
        self.success = success
        self.payload = payload
        self.message = message
