from typing import Optional, Any

class Nexilum_error(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, response: Any = None):
        # Initializes the Integration_error exception with a message, status code, and an optional response.
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)