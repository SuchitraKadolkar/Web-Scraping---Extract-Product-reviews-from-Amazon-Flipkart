FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static website files to nginx default path
COPY ./index.html /usr/share/nginx/html/
