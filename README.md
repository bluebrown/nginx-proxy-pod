#  Nginx Proxy Pod

Example pod configuration for micro service architecture.

- Nginx
- Mongo DB
- Memcache
- Python Rest API
- Tomcat 9

## Quick Start

### Building the Images

```shell
podman build -t fastapi python-api/
podman build -t tomcat:custom tomcat/
podman build -t mongo:custom mongo/  
```

### Starting the Pod

If you pulled the repository to a different location than `$HOME/podman/nginx-proxy-pod`,
you need edit the volume location in the pod.yaml before running the below command.

```shell
podman play kube pod.yml
```

Once the pod is running the below resources are available amogst others.

- [Nginx](http://127.0.0.1:8080)
- [API Docs](http://localhost:8080/api/docs)
- [Tomcat](http://localhost:8080/tomcat/docs)

## Setup

### Creating a Pod

```shell
podman pod create --name playground -p 8080:80
```

### Nginx

```shell
podman run --rm -d -ti --pod playground --name nginx \
  -v $PWD/nginx/conf.d:/etc/nginx/conf.d:Z \
  nginx
```

### Memcache

```shell
podman run --rm -d -ti --name memcache --pod playground memcached
```

### Mongo DB

Since a persistent volume is mapped, the init env variables have only affect when the volume hasn't been used before
and the container starts for the first time.

```shell
podman run --rm -d -ti --name mongo --pod playground \
  -v $PWD/mongo/data:/data/db:Z \
  -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  -e MONGO_INITDB_DATABASE=admin \
  mongo:custom
```

### FastAPI

```shell
podman run --rm -d -ti --pod playground --name fastapi -v $PWD/python-api/app:/app:Z fastapi
```

### Tomcat

```shell
podman run --rm -d -ti --pod playground --name tomcat \
  -v $PWD/tomcat/tomcat-users.xml:/usr/local/tomcat/conf/tomcat-users.xml:Z \
  -v $PWD/tomcat/context.xml:/usr/local/tomcat/conf/context.xml:Z \
  tomcat:custom
```

## Kube

Read more on the pod.yaml in [this article](https://www.redhat.com/sysadmin/compose-podman-pods)

### Generate Pod Yaml

```shell
podman generate kube playground >> ./pod.yaml
```

Don't forget to append `:Z` to each mount path, if you are on selinux. I.E.

```yaml
...
volumeMounts:
  - mountPath: /etc/nginx/conf.d:Z
    name: home-blue-nginx-proxy-pod-nginx-conf.d
...
```

