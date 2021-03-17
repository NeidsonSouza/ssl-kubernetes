#!/bin/bash

CERTBOT="docker run --rm -ti -v $(pwd)/letsencrypt:/etc/letsencrypt certbot/dns-cloudflare"
DOMAIN=$1
SERVER=$2

echo Gerando certificado wildcard SSL para o domÃ­nio $DOMAIN

if [ -z $DOMAIN ]; then
  echo You must inform a domain to generate a SSL
  echo Try $0 DOMAIN PATH
  exit 1
fi

mkdir -p /tmp/letsencrypt/$DOMAIN

echo $CERTBOT

$CERTBOT certonly \
  --non-interactive \
  --email dominios@wisereducacao.com \
  --server $SERVER \
  --dns-cloudflare \
  --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini \
  --dns-cloudflare-propagation-seconds 120 \
  --agree-tos \
  -d ${DOMAIN},*.${DOMAIN}

# if [ -z $FOLDER ]; then
#   echo You must copy your new certificates into your working folder like this:
#   echo cp -L ./letsencrypt/live/${DOMAIN}/* ../metadata/[PATH]/ssl/${DOMAIN}
# else
#   cp -L ./letsencrypt/live/${DOMAIN}/* ../metadata/${FOLDER}/ssl/${DOMAIN}
# fi
