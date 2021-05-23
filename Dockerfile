FROM gcr.io/google.com/cloudsdktool/cloud-sdk:338.0.0-slim

ENV ROOT_DIR=/app

RUN apt update && \
    apt install -y \
        certbot=0.31.0-1+deb10u1 kubectl \
        python3-certbot-dns-route53

WORKDIR /app

COPY . /app

RUN pip3 install --upgrade pip && \
    pip install .
RUN rm -r /etc/letsencrypt/
RUN ln -s $(pwd)/letsencrypt/ /etc/
