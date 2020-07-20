FROM python:3.7-alpine AS builder

ENV PYTHONUNBUFFERED 1
WORKDIR /code

RUN apk update && \
    apk add --no-cache jq gcc python-dev build-base libffi-dev && \
    pip install --no-warn-script-location --prefix=/install gunicorn[gevent]

# Install python requirements
COPY Pipfile.lock .
RUN jq -r '.default | to_entries[] | .key + .value.version ' Pipfile.lock > requirements.txt && \
    pip install --no-cache-dir --no-warn-script-location --prefix=/install -Ur requirements.txt


FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
WORKDIR /code

RUN echo "nameserver 8.8.4.4" >> /etc/resolv.conf && \
    apk update && \
    apk add --no-cache npm && \

COPY --from=builder /install /usr/local

COPY config.py manage.py /code/
COPY app/ /code/app/

# next command fix some strange bug of gevent
# details https://github.com/gevent/gevent/issues/941
# though there is problem in SSLContex, which doesn't really relate to our case, however it works somehow anyway
RUN echo 'import gevent.monkey; gevent.monkey.patch_all()' | cat - manage.py > tmp && mv tmp manage.py

EXPOSE 5000

CMD ["gunicorn", "-b", \
        ":5000", \
        "-k", "gevent", \
        "-w", "2", \
        "--access-logfile", "-", \
        "manage:app"]
