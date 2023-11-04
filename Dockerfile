FROM alpine:latest
COPY requirements.txt .

RUN apk update \
 && apk upgrade \
 && apk add tor haproxy privoxy python3 --update-cache --repository http://dl-4.alpinelinux.org/alpine/edge/community/ --allow-untrusted \
 && apk add bash \
 && python3 -m ensurepip && pip3 install -r requirements.txt \
 && rm /var/cache/apk/*

 WORKDIR /
 COPY start.py proxy-list.py /
 COPY proxy/ /proxy
 COPY templates/ /templates
 RUN /bin/sh -c chmod +x *.py
 EXPOSE 1080/tcp 2090/tcp 8800/tcp 8888/tcp
 CMD "/bin/sh" "-c" "./start.py"