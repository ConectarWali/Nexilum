from http import HTTPMethod
from requests import RequestException, Session, HTTPError
from logging import getLogger
from typing import Optional, Dict, Any

from exception_nexilum.nexilum_error import Nexilum_error

class Nexilum:
    DEFAULT_TIMEOUT = 30  # Default timeout for requests (in seconds)
    MAX_RETRIES = 3  # Maximum number of retries for failed requests

    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = DEFAULT_TIMEOUT,
        verify_ssl: bool = True
    ):
        # Initializes the Integrations with base URL, headers, parameters, timeout, and SSL verification flag.
        self.__base_url = base_url.rstrip('/')
        self.__headers = headers or {}
        self.__params = params or {}
        self.__timeout = timeout
        self.__verify_ssl = verify_ssl
        self.__logger = getLogger(__name__)
        # Create a session for connection pooling and persistent settings
        self.__session = Session()
        self.__session.headers.update(self.__headers)
        
    def __enter__(self):
        # Allows the use of this class in a context manager (with statement)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Handles exceptions when exiting the context manager and logs errors if necessary.
        if exc_type:
            self.__logger.error(f"Error: {exc_val}")
        # Close the session when exiting the context manager
        self.__session.close()
        return False
    
    @property
    def base_url(self) -> str: return self.__base_url

    @base_url.setter
    def base_url(self, value: str) -> None: self.__base_url = value
    
    def update_headers(self, headers: Dict[str, str]) -> None:
        self.__headers.update(headers)
        self.__session.headers.update(headers)
    
    def headers(self) ->  Dict[str, str]: return self.__headers
    
    def delete_headers(self) ->  None:  
        self.__headers.update({})
        self.__session.headers.update({})

    def request(
        self,
        method: HTTPMethod,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        retry_count: int = 0,
    ) -> Optional[Dict[str, Any]]:
        # Sends an HTTP request to the specified endpoint with the given method and data.
        url = self._build_url(endpoint)
        
        # Combine default params with request-specific params
        all_params = {**self.__params, **(params or {})}
        
        try:
            # Use requests library instead of urllib
            response = self.__session.request(
                method=method.value,
                url=url,
                json=data,  # Use json parameter for automatic JSON encoding
                params=all_params,
                timeout=self.__timeout,
                verify=self.__verify_ssl
            )
            
            # Raise HTTP errors
            response.raise_for_status()
            
            # Return the JSON response
            return response.json()
                
        except HTTPError as e:
            # Retries the request if it's a server error (5xx) and retry count is less than MAX_RETRIES
            if retry_count < self.MAX_RETRIES and 500 <= e.response.status_code < 600:
                self.__logger.warning(f"Retrying request due to server error: {e}")
                return self.request(method, endpoint, data, params, retry_count + 1)
            
            error_msg = f"{e.response.status_code} {e.response.reason}"
            self.__logger.error(error_msg)
            self.__logger.error(f"Response content: {e.response.text}")
            raise Nexilum_error(error_msg, e.response.status_code)
            
        except RequestException as e:
            # Handle other request exceptions
            error_msg = f"Request failed: {str(e)}"
            self.__logger.error(error_msg)
            raise Nexilum_error(error_msg)

    def _build_url(self, endpoint: str) -> str:
        return f"{self.__base_url}/{endpoint.lstrip('/')}"