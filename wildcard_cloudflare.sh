#!/bin/bash

DOMAIN=$1

echo Gerando certificado wildcard SSL para o dominio $DOMAIN

if [ -z $DOMAIN ]; then
  echo You must inform a domain to generate a SSL
  echo Try $0 DOMAIN PATH
  exit 1
fi

mkdir -p /tmp/letsencrypt/$DOMAIN

certbot certonly \
  --non-interactive \
  --email dominios@wisereducacao.com \
  --server $SERVER \
  --dns-cloudflare \
  --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini \
  --dns-cloudflare-propagation-seconds 120 \
  --agree-tos \
  -d ${DOMAIN},*.${DOMAIN}
