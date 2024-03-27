FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y gcc \
      libhdf5-serial-dev \
      netcdf-bin \
      libnetcdf-dev

COPY . /app
WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=/root/.local/bin:$PATH
RUN poetry install

COPY . /app

EXPOSE 5000
CMD ["poetry", "run", "gunicorn", "--timeout", "600", "--bind=0.0.0.0:5000", "orca:create_app()"]
