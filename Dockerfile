FROM python:3.7-alpine
LABEL maintainer="ressetkk@gmail.com"

ARG VERSION
ENV VERSION=$VERSION

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN apk --no-cache add libc-dev
RUN pip install -r requirements.txt

COPY . /app

CMD ["gunicorn", "-b 127.0.0.1:2137", "app"]