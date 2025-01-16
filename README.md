# HTTP Integration Library Documentation

A Python library for simplifying HTTP integrations with REST APIs, featuring decorators for authentication handling and request management.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Components](#components)
- [Usage](#usage)
- [Example Implementation](#example-implementation)
- [API Documentation](#api-documentation)

## Features

- Decorator-based HTTP integration setup
- Automatic authentication management
- Request retry mechanism for server errors
- SSL verification support
- Flexible header and parameter management
- Context manager support

## Installation

```bash
pip install integration
```

## Components

### Integration Class

The core class handling HTTP requests and responses.

#### Key Features:

- Configurable base URL, headers, and parameters
- SSL verification toggle
- Custom timeout settings
- Automatic retry mechanism for failed requests
- JSON request/response handling

### Decorators

#### @connect_to

Main decorator for connecting a class to an HTTP integration.

```python
@connect_to(
    base_url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    verify_ssl: bool = True
)
```

#### @login

Handles authentication and token management.

```python
@login
def login_method(self, **kwargs):
    pass
```

#### @logout

Manages session termination and token cleanup.

```python
@logout
def logout_method(self, **kwargs):
    pass
```

#### @auth

Ensures authentication before method execution.

```python
@auth
def protected_method(self, **kwargs):
    pass
```

## Usage

1. Import required components:
```python
from http import HTTPMethod
from integration import connect_to
```

2. Create a decorated class:
```python
@connect_to(base_url="https://api.example.com", headers={"Content-Type": "application/json"})
class APIClient:
    def get_resource(self, method=HTTPMethod.GET, endpoint="resource", **data):
        pass
```

3. Initialize and use the client:
```python
client = APIClient()
response = client.get_resource()
```

## Example Implementation

Below is a complete example using the JSONPlaceholder API:

```python
from http import HTTPMethod
from utils_cws_web import connect_to

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

Example usage:

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

## API Documentation

### Integration Class Methods

#### `__init__(base_url, headers=None, params=None, timeout=30, verify_ssl=True)`

Initialize a new Integration instance.

Parameters:
- `base_url`: Base URL for the API
- `headers`: Optional dictionary of HTTP headers
- `params`: Optional dictionary of query parameters
- `timeout`: Request timeout in seconds
- `verify_ssl`: Boolean to enable/disable SSL verification

#### `request(method, endpoint, data=None, params=None, retry_count=0)`

Send an HTTP request.

Parameters:
- `method`: HTTP method (GET, POST, etc.)
- `endpoint`: API endpoint
- `data`: Optional request body
- `params`: Optional query parameters
- `retry_count`: Current retry attempt number

Returns:
- Dictionary containing the JSON response

### Error Handling

The library includes a custom `Integration_error` exception class for handling HTTP-related errors. All HTTP errors are wrapped in this exception class with appropriate error messages and status codes.

## Best Practices

1. Always use type hints for better code maintainability
2. Handle exceptions appropriately in your implementation
3. Use the context manager when possible
4. Configure appropriate timeout values for your use case
5. Consider SSL verification requirements for your environment

## Contributing

Guidelines for contributing to the project would go here.

## License

License information would go here.