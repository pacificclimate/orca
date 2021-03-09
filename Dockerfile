FROM python:3.8-slim

ENV PIP_INDEX_URL="https://pypi.pacificclimate.org/simple/"

RUN apt-get update && \
    apt-get install -y gcc \
      libpq-dev \
      libhdf5-serial-dev \
      netcdf-bin \
      libnetcdf-dev

COPY . /app

WORKDIR /app

RUN pip install -U pip && \
    pip install -r requirements.txt && \
    pip install waitress && \
    pip install -e .

COPY . /app

EXPOSE 5000
CMD ["waitress-serve", "orca:create_app"]
