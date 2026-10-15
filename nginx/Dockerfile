FROM nginx:1.27-alpine

# gettext provides envsubst, used to inject API_KEY into the nginx config
# at container start without baking it into the image.
RUN apk add --no-cache gettext

COPY index.html app.js /usr/share/nginx/html/
COPY nginx.conf.template /etc/nginx/templates/nginx.conf.template
COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/docker-entrypoint.sh"]
