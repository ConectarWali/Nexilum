# 🌐 Nexilum Library Documentation

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A Python library for simplifying HTTP integrations with REST APIs, featuring decorators for authentication handling and request management.

## Table of Contents

- [🚀 Features](#-features)
- [📦 Installation](#-installation)
- [🔧 Components](#-components)
- [📘 Usage](#-usage)
- [💻 Example Implementation](#-example-implementation)
- [📚 API Documentation](#-api-documentation)
- [⚡ Best Practices](#-best-practices)

## 🚀 Features

- ✨ Decorator-based HTTP integration setup
- 🔐 Automatic authentication management
- 🔄 Request retry mechanism for server errors (up to 3 retries)
- 🛡️ SSL verification support
- 📝 Flexible header and parameter management
- ⚡ Context manager support
- 🔍 Comprehensive error handling

## 📦 Installation

```bash
pip install nexilum
```

## 🔧 Components

### Nexilum Class

The core class handling HTTP requests and responses:

```python
from nexilum import Nexilum

client = Nexilum(
    base_url="https://api.example.com",
    headers={"Content-Type": "application/json"},
    timeout=30,
    verify_ssl=True
)
```

#### Key Features:

- 🔗 Configurable base URL, headers, and parameters
- 🛡️ SSL verification toggle
- ⏱️ Custom timeout settings (default: 30 seconds)
- 🔄 Automatic retry mechanism for 5xx errors
- 📝 JSON request/response handling

### Decorators

#### @connect_to

```python
@connect_to(
    base_url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = DEFAULT_TIMEOUT,
    verify_ssl: bool = True
)
```

Main decorator for connecting a class to an HTTP integration.

#### @login

```python
@login
def authenticate(self, **kwargs):
    """
    Handle authentication and token management.
    Returns the authentication response or None if already authenticated.
    """
    pass
```

#### @logout

```python
@logout
def end_session(self, **kwargs):
    """
    Manage session termination and token cleanup.
    Returns the logout response or None if already logged out.
    """
    pass
```

#### @auth

```python
@auth
def protected_endpoint(self, **kwargs):
    """
    Ensure authentication before method execution.
    Automatically handles re-authentication if needed.
    """
    pass
```

## 📘 Usage

### Basic Setup

```python
from http import HTTPMethod
from nexilum import Nexilum, connect_to
```

### Error Handling

```python
from nexilum.exceptions import Nexilum_error

try:
    with Nexilum(base_url="https://api.example.com") as client:
        response = client.request(
            method=HTTPMethod.GET,
            endpoint="users"
        )
except Nexilum_error as e:
    print(f"Error occurred: {e}")
```

## 💻 Example Implementation

### Class-Based Implementation

```python
@connect_to(
    base_url="https://api.example.com",
    headers={"Content-Type": "application/json"}
)
class APIClient:
    @login
    def authenticate(self, credentials):
        pass

    @auth
    def get_resource(self, resource_id):
        pass

    @logout
    def end_session(self):
        pass
```

### Direct Usage

```python
with Nexilum(base_url="https://api.example.com") as client:
    # GET request
    users = client.request(
        method=HTTPMethod.GET,
        endpoint="users",
        params={"page": 1}
    )

    # POST request
    new_user = client.request(
        method=HTTPMethod.POST,
        endpoint="users",
        data={
            "name": "John Doe",
            "email": "john@example.com"
        }
    )
```

## 📚 API Documentation

### Nexilum Class

#### Constructor Parameters

| Parameter   | Type    | Required | Default | Description                    |
|------------|---------|----------|---------|--------------------------------|
| base_url   | str     | Yes      | -       | Base API URL                   |
| headers    | Dict    | No       | None    | Default request headers        |
| params     | Dict    | No       | None    | Default query parameters       |
| timeout    | int     | No       | 30      | Request timeout in seconds     |
| verify_ssl | bool    | No       | True    | SSL verification flag          |

#### Methods

##### request()

```python
def request(
    self,
    method: HTTPMethod,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    retry_count: int = 0
) -> Optional[Dict[str, Any]]
```

Parameters:
- `method`: HTTP method (GET, POST, etc.)
- `endpoint`: API endpoint
- `data`: Request body (optional)
- `params`: Query parameters (optional)
- `retry_count`: Current retry attempt (internal use)

### Error Handling

The `Nexilum_error` class provides structured error information:

```python
class Nexilum_error(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
```

## ⚡ Best Practices

1. **Use Type Hints**
   ```python
   from typing import Dict, Optional
   ```

2. **Context Managers**
   ```python
   with Nexilum(base_url="https://api.example.com") as client:
       # Your code here
   ```

3. **Error Handling**
   ```python
   try:
       response = client.request(...)
   except Nexilum_error as e:
       if e.status_code == 404:
           # Handle not found
   ```

4. **Security**
   - Enable SSL verification in production
   - Store sensitive credentials securely
   - Use environment variables for configuration

5. **Performance**
   - Configure appropriate timeout values
   - Handle rate limiting appropriately
   - Use connection pooling when available

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by the Nexilum team.
