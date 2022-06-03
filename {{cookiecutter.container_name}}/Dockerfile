############################### START NEW IMAGE dev #############################
# Dockerfile
FROM python:3.9.12-alpine as base

ARG FOLDER=/app

WORKDIR ${FOLDER}

COPY Pipfile ./Pipfile.lock ${FOLDER}

COPY ./ ${FOLDER}

RUN pip install --no-cache-dir pipenv && \
  pipenv install --system --deploy --clear

EXPOSE {{cookiecutter.port}}

CMD ["python", "app.py"]