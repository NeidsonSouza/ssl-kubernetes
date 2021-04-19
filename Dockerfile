# FROM python:3.7-slim
FROM gcr.io/google.com/cloudsdktool/cloud-sdk:334.0.0

RUN apt update && \
    apt install -y certbot=0.31.0-1+deb10u1 git

WORKDIR /app

COPY . /app

RUN pip install .
RUN rm -r /etc/letsencrypt/
RUN ln -s $(pwd)/letsencrypt/ /etc/
