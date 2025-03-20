FROM python:3.11-slim-buster

WORKDIR /opt/app

ENV TZ=UTC
ENV PYTHONUNBUFFERED=1

RUN apt update \
    && apt install -y gcc bash \
    && pip3 install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .
ENTRYPOINT ["python", "app.py"]
