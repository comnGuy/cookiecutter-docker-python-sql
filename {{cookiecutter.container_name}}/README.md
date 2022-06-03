# Getting Started

## Docker

1. `docker-compose up --build {{cookiecutter.container_name}}`

_Warning_

- `{{cookiecutter.database_name}}` have to run.

## Python

1. `pipenv install`
2. `pipenv run python app.py` or `pipenv shell` and `python app.py`

_Warning_

- `{{cookiecutter.database_name}}` have to run.

### Docker-compose

Add the following lines to docker-compose

```
  {{cookiecutter.container_name}}:
    build:
      context: ./{{cookiecutter.container_name}}
    image: {{cookiecutter.container_name}}
    restart: always
    volumes:
      - ./{{cookiecutter.container_name}}/logs:/app/logs
      - ./{{cookiecutter.container_name}}/:/app
    env_file:
      - ./_env/{{cookiecutter.container_name}}.env
    depends_on:
      - {{cookiecutter.database_name}}
    # LOCAL TESTING
    ports:
      - 3000:3000
```
