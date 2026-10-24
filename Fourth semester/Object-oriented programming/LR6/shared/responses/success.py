class SuccessResponse:
    def __init__(self, code: int, message: str, data):
        self.code = code
        self.message = message
        self.data = data
    
    def to_dict(self):
        data_dict = self.data.to_dict() if hasattr(self.data, 'to_dict') else self.data
        return {
            "code": self.code,
            "message": self.message,
            "data": data_dict
        }
