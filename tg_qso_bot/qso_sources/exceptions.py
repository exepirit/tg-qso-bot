class ServerResponseError(Exception):
    def __init__(self, url: str, status_code: int, message: str = None):
        self.url = url
        self.status_code = status_code
        self.message = message

    def __repr__(self) -> str:
        return f"Server returns code {self.status_code}."


class ParsingError(Exception):
    pass
