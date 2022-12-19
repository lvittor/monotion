FROM python:3.10.0

WORKDIR /code

ENV POETRY_VERSION=1.1.13

# Install system deps
RUN apt-get update && \
    apt-get install -y libblas-dev liblapack-dev g++ gfortran cmake swig graphviz graphviz-dev && \
    pip install -U pip && \
    pip install psycopg2-binary==2.9.3

# Install Python env
RUN pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false
COPY ./pyproject.toml /code/
COPY ./poetry.lock /code/
RUN poetry install

COPY . /code

CMD ["poetry", "run", "uvicorn", "app.main:app", "--log-level", "debug", "--reload", "--host", "0.0.0.0", "--port", "80"]