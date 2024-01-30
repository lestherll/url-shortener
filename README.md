# Liit 

[![Tests](https://github.com/lestherll/url-shortener/actions/workflows/python-app.yml/badge.svg)](https://github.com/lestherll/url-shortener/actions/workflows/python-app.yml)

Liit (pronounced Li-it, Filipino word for little) is a minimal URL Shortener API written in Python using FastAPI.


# Design
|               |            |
|---------------|------------|
| **Server**    | FastAPI    |
| **Cache**     | memcached  |
| **Database**  | PostgreSQL |

# Running the application 
This project has been developed with `poetry` in mind, and thus should be more convenient to use with `poetry`.
Running the project is as simple as:
```
poetry run uvicorn url_shortener.main:app
```

# Running tests
```
python -m pytest
```
