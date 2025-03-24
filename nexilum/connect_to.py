from functools import wraps
from http import HTTPMethod
from inspect import signature
from typing import Callable, Dict, Optional, Type, TypeVar
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
            self._integration:Nexilum = Nexilum(base_url=base_url, headers=headers, params=params, timeout=timeout, verify_ssl=verify_ssl)
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
    """
    Transforma un método para que use la integración HTTP, sin lógica en el método de la clase.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        method_signature = signature(method)
        parameters = method_signature.parameters

        http_method = kwargs.pop("method", parameters.get("method", {}).default)
        value = kwargs.pop("value", parameters.get("value").default if parameters.get("value") else '')
        endpoint = kwargs.pop("endpoint", parameters.get("endpoint").default if parameters.get("endpoint") else None)
        params = kwargs.pop("params", parameters.get("params").default if parameters.get("params") else {})
        headers = kwargs.pop("headers", parameters.get("headers").default if parameters.get("headers") else {})
        no_headers = kwargs.pop("no_headers", parameters.get("no_headers").default if parameters.get("no_headers") else [])
        custom_headers = kwargs.pop("custom_headers", parameters.get("custom_headers").default if parameters.get("custom_headers") else {})
        data = kwargs.pop("data", None)

        # Validar que el 'endpoint' esté presente
        if not endpoint:
            raise ValueError(f"No se especificó un endpoint para el método {method.__name__}")
        if not isinstance(endpoint, str):
            raise ValueError(f"El endpoint especificado no es de tipo cadena para el método {method.__name__}")
        if not isinstance(http_method, HTTPMethod):
            raise ValueError(f"El http_method especificado no es de tipo HTTPMethod para el método {method.__name__}")

        if headers:
            self._integration.update_headers(headers)
        if no_headers:
            current_headers = self._integration.headers()
            for header in no_headers:
                if header in current_headers:
                    current_headers.pop(header)
            self._integration.delete_headers()
            self._integration.update_headers(current_headers)
        if custom_headers:
            self._integration.delete_headers()
            self._integration.update_headers(custom_headers)
        if hasattr(self, '_token') and self._token:
            self._integration.update_headers({'Authorization': f"Bearer {self._token}"})

        if endpoint.endswith('/'):
            endpoint = f"{endpoint}{value}"
        else:
            endpoint = f"{endpoint}/{value}"


        # Realizar la solicitud HTTP y retornar la respuesta
        response = self._integration.request(
            method=http_method,  # Usar el valor de la enumeración
            endpoint=endpoint,
            data=data,
            params=params
        )
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
