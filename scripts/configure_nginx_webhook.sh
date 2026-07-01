#!/usr/bin/env bash
set -euo pipefail

cat > /etc/nginx/sites-available/devin-investment-os <<'NGINX'
server {
    listen 80;
    server_name 45.32.52.205;

    location = /tradingview-webhook {
        proxy_pass http://127.0.0.1:8502/tradingview-webhook;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
NGINX

ln -sf /etc/nginx/sites-available/devin-investment-os /etc/nginx/sites-enabled/devin-investment-os
nginx -t
systemctl restart nginx
