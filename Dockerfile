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
COPY static/* /var/www/html/
RUN mv entrypoint.sh / && chmod +x /entrypoint.sh \
    && rm -rf static nginx.conf
# CMD ["gunicorn", "-b 0.0.0.0:80", "wsgi:app"]
# CMD ["uwsgi", "--http", "0.0.0.0:5000","--module", "app"]
# CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
CMD ["/entrypoint.sh"]