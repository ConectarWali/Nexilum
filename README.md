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
def authenticate(self, method=HTTPMethod.POST, endpoint="login", **data):
    """
    Handle authentication and token management.
    Returns the authentication response or None if already authenticated.
    """
    pass
```

#### @logout

```python
@logout
def end_session(self, method=HTTPMethod.POST, endpoint="end_session", **data):
    """
    Manage session termination and token cleanup.
    Returns the logout response or None if already logged out.
    """
    pass
```

#### @auth

```python
@auth
def protected_endpoint(self, endpoint="end_session", method=HTTPMethod.GET, **data):
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
from http import HTTPMethod
from nexilum import connect_to

@connect_to(
    base_url="https://jsonplaceholder.typicode.com", 
    headers={"Content-Type": "application/json"}
)
class JSONPlaceholder:
    def get_posts(self, method=HTTPMethod.GET, endpoint="posts", **data):
        pass

    def get_post(self, method=HTTPMethod.GET, endpoint="posts/{post_id}", **data):
        pass

    def get_post_comments(self, method=HTTPMethod.GET, endpoint="posts/{post_id}/comments", **data):
        pass

    def create_post(self, method=HTTPMethod.POST, endpoint="posts", **data):
        pass

    def update_post(self, method=HTTPMethod.PUT, endpoint="posts/{post_id}", **data):
        pass

    def delete_post(self, method=HTTPMethod.DELETE, endpoint="posts/{post_id}", **data):
        pass

    def get_users(self, method=HTTPMethod.GET, endpoint="users", **data):
        pass

    def get_user(self, endpoint:str, method=HTTPMethod.GET, **data):
        pass

    def get_user_posts(self, method=HTTPMethod.GET, endpoint="users/{user_id}/posts", **data):
        pass

    def get_user_todos(self, method=HTTPMethod.GET, endpoint="users/{user_id}/todos", **data):
        pass
```

Example usage with decorators:

```python
# Initialize client
api = JSONPlaceholder()

# Get all posts
posts = api.get_posts()

# Get specific post
post = api.get_post(endpoint="posts/1")

# Create new post
new_post = api.create_post(data={
    "title": "foo",
    "body": "bar",
    "userId": 1
})

# Update post
updated_post = api.update_post(
    endpoint="posts/1",
    data={
        "id": 1,
        "title": "foo updated",
        "body": "bar updated",
        "userId": 1
    }
)

# Delete post
deleted = api.delete_post(endpoint="posts/1")

# Get users
users = api.get_users()

# Get specific user
user = api.get_user(endpoint="users/1")
```

### Direct Usage

```python
from http import HTTPMethod
from nexilum import Nexilum

# Initialize the Nexilum instance
api = Nexilum(
    base_url="https://jsonplaceholder.typicode.com",
    headers={"Content-Type": "application/json"}
)

# Using the context manager for safe resource handling
with api as client:
    # Get all posts
    posts = client.request(
        method=HTTPMethod.GET,
        endpoint="posts"
    )

    # Get specific post
    post = client.request(
        method=HTTPMethod.GET,
        endpoint="posts/1"
    )

    # Create new post
    new_post = client.request(
        method=HTTPMethod.POST,
        endpoint="posts",
        data={
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
    )

    # Update post
    updated_post = client.request(
        method=HTTPMethod.PUT,
        endpoint="posts/1",
        data={
            "id": 1,
            "title": "foo updated",
            "body": "bar updated",
            "userId": 1
        }
    )

    # Delete post
    deleted = client.request(
        method=HTTPMethod.DELETE,
        endpoint="posts/1"
    )

    # Get users
    users = client.request(
        method=HTTPMethod.GET,
        endpoint="users"
    )

    # Get specific user
    user = client.request(
        method=HTTPMethod.GET,
        endpoint="users/1"
    )

# Example with error handling
try:
    with Nexilum(base_url="https://jsonplaceholder.typicode.com") as client:
        response = client.request(
            method=HTTPMethod.GET,
            endpoint="nonexistent"
        )
except Nexilum_error as e:
    print(f"Error occurred: {e}")
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
    def __init__(self, message: str, status_code: Optional[int] = None, response: Any = None):
        self.message = message
        self.status_code = status_code
        self.response = response
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
