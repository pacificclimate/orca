FROM python:3.8-slim

ENV PIP_INDEX_URL="https://pypi.pacificclimate.org/simple/"
ENV LDFLAGS="-L/usr/local/opt/openssl/lib"
ENV CPPFLAGS="-I/usr/local/opt/openssl/include"

RUN apt-get update && \
    apt-get install -y gcc libpq-dev libhdf5-serial-dev netcdf-bin libnetcdf-dev

COPY . /app

WORKDIR /app

RUN pip install -U pip && \
    pip install -r requirements.txt && \
    pip install -e .

COPY . /app

CMD ["python", "orca/app.py"]
