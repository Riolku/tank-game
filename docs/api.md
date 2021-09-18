# API Routing

## API response format
- success:
```json
{
    "result":"ok",
    "data":{...}
}
```
- failure:
 - make sure to send err code
```json
{
    "result":"ko",
    "error":{
        "title":"http_error_of_some_kind",
        "description":"http error description"
    }
}
```

## API jwt auth key
- format:
```json
{
    "uuid":"user uuid string",
}
```

## Endpoints
### /api/auth/login : POST
- request:
```json
{
    "username":"string",
    "password":"password"
}
```
- response:
 - set jwt token as cookie
```json
{
    "result":"ok",
}
```

### /api/auth/register : POST
- request:
```json
{
    "username":"string",
    "password":"password"
}
```
- response:
```json
{
    "result":"ok",
}
```

### /api/user/<uid> : GET
- get general information about user to help with frontend (username/other personalization shit (settings if we want))

### /api/user/<uid>/teams : GET : auth
- get specified user's teams
 - requires authentication

### /api/user/<uid>/ai : GET : auth

### /api/ai/submit : POST

- submit ai

- reqeust:
```json
{
    "name":"string",
    "data":"bytes or smth idk LOL"
}
```
