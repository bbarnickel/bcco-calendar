FROM alpine:latest

WORKDIR /var/www/app

RUN apk add --no-cache \
        uwsgi-python3 \
        python3

#RUN adduser -H uwsgi

COPY ./requirements.txt .
RUN pip3 install \
    --upgrade pip \
    --no-cache-dir \
    -r requirements.txt

RUN mkdir /var/www/app/data ; \
    chown uwsgi:uwsgi /var/www/app/data 

COPY ./uwsgi.ini ./
COPY ./*.py ./
CMD [ "uwsgi", "uwsgi.ini"]
