#!/bin/sh
set -eu

: "${API_KEY:?API_KEY environment variable must be set (e.g. via docker-compose --env-file .env)}"
: "${API_UPSTREAM:?API_UPSTREAM environment variable must be set}"

# Only substitute the variables we control so nginx's own variables remain intact.
envsubst '${API_KEY} ${API_UPSTREAM}' \
  < /etc/nginx/templates/nginx.conf.template \
  > /etc/nginx/conf.d/default.conf

exec nginx -g 'daemon off;'
