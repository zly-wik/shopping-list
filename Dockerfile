FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /shoppinglist
WORKDIR /shoppinglist

COPY . /shoppinglist

RUN pip install --upgrade pip
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

