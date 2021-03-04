FROM python:3.8-slim

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip upgrade -U pip && \
    pip install -r requirements.txt && \
    pip install -e .

COPY . /app

ENTRYPOINT ["python"]
CMD ["orca/app.py"]
