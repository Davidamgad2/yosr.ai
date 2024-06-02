FROM python:3.11.6-alpine3.18
LABEL maintainer="David Amgad"

WORKDIR /warehouse


ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY . .


EXPOSE 8000
EXPOSE 5432

RUN python -m venv /py && \
/py/bin/pip install --upgrade pip
RUN    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
    build-base postgresql-dev musl-dev linux-headers libpq-dev && \
    apk del .tmp-deps
RUN    /py/bin/pip install -r /requirements.txt
RUN   adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x ./run.sh
ENV PATH="/py/bin:$PATH"

CMD ["./run.sh"]
