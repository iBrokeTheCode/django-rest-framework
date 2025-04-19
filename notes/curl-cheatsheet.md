# cURL Guide for API Testing and Debugging

This guide covers how to use `curl` to test and debug API endpoints in Django REST Framework (DRF). It includes requests for the main HTTP methods and common cases like authentication, headers, and JSON payloads.

## 1. GET Requests

### Basic GET request

```bash
curl http://localhost:8000/api/posts/
```

### With query parameters

```bash
curl "http://localhost:8000/api/posts/?search=python&page=2"
```

### With custom headers

```bash
curl -H "Accept: application/json" http://localhost:8000/api/posts/
```

## 2. POST Requests

### Basic POST with JSON body

```bash
curl -X POST http://localhost:8000/api/posts/ \
     -H "Content-Type: application/json" \
     -d '{"title": "New Post", "content": "This is a test"}'
```

### Posting with authentication

```bash
curl -X POST http://localhost:8000/api/posts/ \
     -H "Authorization: Token your_token_here" \
     -H "Content-Type: application/json" \
     -d '{"title": "Auth Post", "content": "Authenticated!"}'
```

## 3. PUT/PATCH Requests

### Full update with PUT

```bash
curl -X PUT http://localhost:8000/api/posts/5/ \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated Post", "content": "All fields updated"}'
```

### Partial update with PATCH

```bash
curl -X PATCH http://localhost:8000/api/posts/5/ \
     -H "Content-Type: application/json" \
     -d '{"title": "Partially updated title"}'
```

## 4. DELETE Requests

### Delete a resource

```bash
curl -X DELETE http://localhost:8000/api/posts/5/
```

### Delete with auth token

```bash
curl -X DELETE http://localhost:8000/api/posts/5/ \
     -H "Authorization: Token your_token_here"
```

## 5. Authentication

### Basic Authentication

```shell
curl -u username:password http://127.0.0.1:8000/api/protected/
```

### Token Authentication (DRF `TokenAuthentication`)

#### Obtain a token

```bash
curl -X POST http://localhost:8000/api/token/ \
     -d "username=admin&password=yourpassword"
```

#### Use the token in requests

```bash
curl http://localhost:8000/api/posts/ \
     -H "Authorization: Token your_token_here"
```

## 6. JWT Authentication (DRF Simple JWT)

### Get JWT token pair (access + refresh)

```bash
curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "yourpassword"}'
```

### Use JWT access token

```bash
curl http://localhost:8000/api/posts/ \
     -H "Authorization: Bearer your_access_token"
```

### Refresh token

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "your_refresh_token"}'
```

## 7. Debugging Tips

### View full request/response including headers

```bash
curl -v http://localhost:8000/api/posts/

# optional
curl -i http://localhost:8000/api/posts/
```

### Show only response headers

```bash
curl -I http://localhost:8000/api/posts/
```

### Save response to a file

```bash
curl -o response.json http://localhost:8000/api/posts/
```

## 8. Multipart/Form-Data Upload

### Uploading a file (image, etc.)

```bash
curl -X POST http://localhost:8000/api/upload/ \
     -H "Authorization: Token your_token_here" \
     -F "title=File title" \
     -F "file=@/path/to/your/file.jpg"
```

## 9. Custom Headers

```bash
curl http://localhost:8000/api/posts/ \
     -H "X-Custom-Header: custom-value" \
     -H "Authorization: Token your_token_here"
```

## 10. Common DRF Errors

| Status | Meaning               | Cause                                   |
| ------ | --------------------- | --------------------------------------- |
| 400    | Bad Request           | Invalid data format or missing fields   |
| 401    | Unauthorized          | Missing or invalid authentication token |
| 403    | Forbidden             | Authenticated but lacking permissions   |
| 404    | Not Found             | Resource does not exist                 |
| 500    | Internal Server Error | Server-side bug (check logs!)           |

## Pro Tip: Alias for easier use

```bash
alias curljson='curl -H "Content-Type: application/json" -H "Accept: application/json"'
```

## References

- [Django REST Framework Auth](https://www.django-rest-framework.org/api-guide/authentication/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [curl Manual](https://curl.se/docs/manpage.html)
