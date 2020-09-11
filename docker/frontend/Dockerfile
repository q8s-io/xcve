FROM node:14 as builder

COPY ./fe /opt/app

RUN cd /opt/app && \
    yarn && \
    npm run build

# build server
FROM nginx:1.18

COPY --from=builder /opt/public/ /usr/share/nginx/html/

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

CMD [nginx-debug, '-g', 'daemon off;']