FROM python:3.8-slim

ENV PIP_INDEX_URL="https://pypi.pacificclimate.org/simple/"

RUN apt-get update && \
    apt-get install -y gcc \
      libhdf5-serial-dev \
      netcdf-bin \
      libnetcdf-dev

COPY . /app
WORKDIR /app

RUN pip install pipenv==2022.10.25 && \
    pipenv install 

COPY . /app

EXPOSE 5000
CMD ["pipenv", "run", "gunicorn", "--timeout", "0", "--bind=0.0.0.0:5000", "orca:create_app()"]
