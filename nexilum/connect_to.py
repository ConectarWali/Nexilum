from functools import wraps
from http import HTTPMethod
from inspect import signature
from urllib.parse import urljoin
from typing import Callable, Dict, List, Optional, Type, TypeVar
from nexilum.nexilum import Nexilum


# Definir un tipo genérico T que representará la clase original
T = TypeVar('T', bound=object)
DEFAULT_TIMEOUT = 30

def connect_to(base_url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        timeout: int = DEFAULT_TIMEOUT,
        verify_ssl: bool = True,
        token:Optional[str] = None,
        credentials: Optional[Dict[str, str]] = None
        ):
    """
    Decorador para conectar una clase a una integración HTTP.
    """
    def decorator(cls: Type[T]) -> Type[T]:
        # Guardar el constructor original
        original_init = cls.__init__

        @wraps(original_init)
        def new_init(self: T, *args, **kwargs):
            # Configurar integración en la instancia
            self._integration = Nexilum(base_url=base_url, headers=headers, params=params, timeout=timeout, verify_ssl=verify_ssl)
            self._token = token if token else None
            self._is_logged_in = False
            self._login_method = getattr(self, "login", None)
            self._logout_method = getattr(self, "logout", None)
            self._credentials = credentials if credentials else None
            # Llamar al constructor original
            original_init(self, *args, **kwargs)

        cls.__init__ = new_init

        # Decorar los métodos de la clase con la integración
        for attr_name in dir(cls):
            if not attr_name.startswith("__"):  # Ignorar métodos mágicos
                attr_value = getattr(cls, attr_name)
                if callable(attr_value):  # Aplicar el decorador a métodos válidos
                    setattr(cls, attr_name, _make_integration_method(attr_value))

        # Retornar la clase decorada, con el tipo correcto
        return cls

    return decorator


def _make_integration_method(method: Callable) -> Callable:
    """Transforma un método para que use la integración HTTP, sin lógica en el método de la clase."""
    
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        method_signature = signature(method)
        parameters = method_signature.parameters

        # Extraer argumentos con valores por defecto
        def get_arg(name, default=""):
            return kwargs.pop(name, parameters.get(name, {}).default if name in parameters else default)

        http_method: HTTPMethod = get_arg("method", HTTPMethod.GET)
        value: str = get_arg("value")
        subdomain: str = get_arg("subdomain")
        prefix: str = get_arg("prefix")
        endpoint: str = get_arg("endpoint", None)
        params: Dict[str, str] = get_arg("params", {})
        headers: Dict[str, str] = get_arg("headers", {})
        no_headers: List[str] = get_arg("no_headers", [])
        custom_headers: Dict[str, str] = get_arg("custom_headers", {})
        data = kwargs.pop("data", None)

        # Validaciones
        if not endpoint or not isinstance(endpoint, str):
            raise ValueError(f"Invalid endpoint: {endpoint}\nMethod: {method.__name__}")
        if not isinstance(http_method, HTTPMethod):
            raise TypeError(f"http_method must be an instance of HTTPMethod\nMethod: {method.__name__}")
        
        valid_types = {"params": dict, "headers": dict, "no_headers": list, "custom_headers": dict}
        for var, expected_type in valid_types.items():
            if not isinstance(locals()[var], expected_type):
                raise TypeError(f"Expected {var} to be {expected_type}, got {type(locals()[var])}\nMethod: {method.__name__}")

        if data is not None and not isinstance(data, dict):
            raise TypeError("data must be a dict or None")

        # Construcción del URL base
        original_url = self._integration.base_url
        base_url = original_url
        protocol = ''
        if subdomain:
            if base_url.startswith('http://'):
                base_url = base_url[7:]
                protocol = 'http://'
            else:
                base_url = base_url[8:]
                protocol = 'https://'
            base_url = f"{subdomain}.{base_url}"
        if prefix:
            base_url = f"{base_url}/{prefix}"
            base_url = f"{protocol}{base_url}"
            
        self._integration.base_url = base_url

        # Manejo de headers
        if headers:
            self._integration.update_headers(headers)
        if no_headers:
            self._integration.delete_headers()
            current_headers = {k: v for k, v in self._integration.headers().items() if k not in no_headers}
            self._integration.update_headers(current_headers)
        if custom_headers:
            self._integration.delete_headers()
            self._integration.update_headers(custom_headers)
        if hasattr(self, '_token') and self._token:
            self._integration.update_headers({'Authorization': f"Bearer {self._token}"})

        # Construcción del endpoint final
        if http_method == HTTPMethod.POST:
            endpoint = urljoin(endpoint, value)
        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            endpoint = f"{endpoint}?{query_string}"

        # Realizar la solicitud HTTP
        response = self._integration.request(
            method=http_method,
            endpoint=endpoint,
            data=data,
            params=params
        )

        # Restaurar URL base original
        self._integration.base_url = original_url
        return response

    return wrapper


def login(method: Callable) -> Callable:
    """
    Decorador para manejar el login y actualizar el estado de autenticación.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self._is_logged_in:
            return None  # Ya está autenticado, no es necesario volver a iniciar sesión

        http_method = kwargs.pop("method", HTTPMethod.POST)
        endpoint = kwargs.pop("endpoint", "login")
        response_param = kwargs.pop("response", "token")
        data = self._credentials if self._credentials else kwargs.pop("data", None) 

        # Realizar la solicitud de login
        response = self._integration.request(
            method=http_method, endpoint=endpoint, data=data
        )
        
        if response and response_param in response:
            self._token = response[response_param]
            self._is_logged_in = True
        else:
            raise RuntimeError("Autenticación fallida: No se recibió el token")

        return response

    return wrapper


def logout(method: Callable) -> Callable:
    """
    Decorador para manejar el logout y limpiar el estado de autenticación.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self._is_logged_in:
            return None  # Ya está desconectado, no es necesario hacer logout

        http_method = kwargs.pop("method", HTTPMethod.POST)
        endpoint = kwargs.pop("endpoint", "logout")
        data = kwargs.pop("data", None)

        # Realizar la solicitud de logout
        response = self._integration.request(
            method=http_method, endpoint=endpoint, data=data
        )
        
        # Limpiar el estado de autenticación
        self._token = None
        self._is_logged_in = False
        return response

    return wrapper


def auth(method: Callable) -> Callable:
    """
    Decorador que asegura autenticación antes de ejecutar un método.
    Si no hay un token válido, intenta iniciar sesión primero.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Si no está autenticado, intenta autenticarse
        if not self._is_logged_in and self._login_method:
            response = self._login_method()
            if response and "token" in response:
                self._token = response["token"]
                self._is_logged_in = True
            else:
                raise RuntimeError("Autenticación fallida")

        try:
            # Llama al método original si la autenticación fue exitosa
            return method(self, *args, **kwargs)
        except Exception as e:
            # Si ocurre un error de autenticación, reintenta una vez
            if "authentication" in str(e).lower() and self._login_method:
                response = self._login_method()
                if response and "token" in response:
                    self._token = response["token"]
                    self._is_logged_in = True
                    return method(self, *args, **kwargs)
            raise e

    return wrapper
