#!/bin/sh
# Railway provides a PORT env variable — we template it into nginx config at startup
PORT=${PORT:-80}
echo "Starting nginx on port $PORT..."

# Replace PORT placeholder in nginx config
sed -i "s/__PORT__/$PORT/g" /etc/nginx/conf.d/default.conf

# Also update the healthcheck URL
echo "Nginx config:"
cat /etc/nginx/conf.d/default.conf

exec nginx -g 'daemon off;'