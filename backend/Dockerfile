FROM python:3.7-alpine
LABEL maintainer="ressetkk@gmail.com"

ARG VERSION
ENV VERSION=$VERSION

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN apk --no-cache add libc-dev nginx \
    && pip install -r requirements.txt \
    && mkdir -p /run/nginx && touch /run/nginx/nginx.pid

COPY . /app
COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN mv entrypoint.sh / && chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]