FROM python:3.8-slim

ENV PIP_INDEX_URL="https://pypi.pacificclimate.org/simple/"

RUN apt-get update && \
    apt-get install -y gcc \
      libhdf5-serial-dev \
      netcdf-bin \
      libnetcdf-dev

COPY . /app

WORKDIR /app

RUN pip install -U pip && \
    pip install -r requirements.txt && \
    pip install gunicorn && \
    pip install -e .

COPY . /app

EXPOSE 5000
CMD ["gunicorn", "--bind=0.0.0.0:5000", "orca:create_app()"]
