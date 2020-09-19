# Server Setup

```shell
podman run --rm -d -p 8080:80 --name nginx \
  -v $PWD/playground/nginx:/etc/nginx/conf.d:Z nginx

podman run -d --rm -p 8888:8080 tomcat
```