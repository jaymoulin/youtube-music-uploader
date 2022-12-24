FROM python:alpine as builder

COPY qemu-*-static /usr/bin/

FROM builder

ARG VERSION=1.3.0

LABEL maintainer="Jay MOULIN <https://jaymoulin.me/me/youtube-music-uploader/> <https://twitter.com/MoulinJay>"
LABEL version=${VERSION}

ENV REMOVE=0
ENV ONESHOT=0
ENV LISTENER_ONLY=0
ENV DEDUP_API=''
ENV ERROR_FILE=''

RUN apk update && \
    apk add gcc g++ linux-headers libxml2-dev libxslt-dev --no-cache --virtual .build-deps && \
    mkdir /root/oauth/ && \
    pip3 install --upgrade pip && \
    pip3 install youtube-music-uploader && \
    apk del gcc --purge .build-deps

COPY ./docker/daemon.sh /root/daemon
COPY ./docker/auth.sh /root/auth

VOLUME /media/library
VOLUME /root/oauth

WORKDIR /root
ENV PATH="/root:${PATH}"
CMD ["daemon"]
