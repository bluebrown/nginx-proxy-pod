# Server Setup

Example pod configuration. Nginx reverse proxy, python api, and tomcat.

## Setup

### Build the docker images

```
podman build -t fastapi python-api/
podman build -t tomcat:custom tomcat/
podman build -t mongo:custom mongo/  
```

### adjust the volume mapping 

In the pod.yaml, change the path for both volumes to the path of the repoistory.

```yaml
...
volumes:
  - hostPath:
      path: /home/blue/nginx-proxy-pod/tomcat/tomcat-users.xml
      type: File
    name: home-blue-nginx-proxy-pod-tomcat-tomcat-users.xml
...
```

Don't forget to append `:Z` to each mount path, if you are on selinux. I.E.

```yaml
...
volumeMounts:
  - mountPath: /etc/nginx/conf.d:Z
    name: home-blue-nginx-proxy-pod-nginx-conf.d
...
```

## Starting the Pod

```shell
podman play kube pod.yml
```

## Visiting the Page

Once the pod is running navigate to http://127.0.0.1:8080, this will open the nginx main page.
Next visit the sample endpoint at /api and the tomcat main page at /tomcat.

## Run individual container

A pod can be created with 

```shell
podman pod create --name playground -p 8080:80
```

### Nginx

```shell
podman run --rm -d -ti --pod playground --name nginx \
  -v $PWD/nginx/conf.d:/etc/nginx/conf.d:Z \
  nginx
```

### FastAPI

```shell
podman run --rm -d -ti --pod playground --name fastapi -v \
  $PWD/python-api/app:/app:Z fastapi
```

### Tomcat

```shell
podman run --rm -d -ti --pod playground --name tomcat \
  -v $PWD/tomcat/tomcat-users.xml:/usr/local/tomcat/conf/tomcat-users.xml:Z \
  -v $PWD/tomcat/context.xml:/usr/local/tomcat/conf/context.xml:Z \
  tomcat:custom
```

### Mongo DB

```shell
podman run --rm -d -ti --pod playground --name mongo \
    -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
    -e MONGO_INITDB_ROOT_PASSWORD=secret \
    -e MONGO_INITDB_DATABASE=admin \
    mongo:custom
```

## Generating a pod.yaml

```shell
podman generate kube playground >> ./pod.yaml
```

Find more info in this [article](https://www.redhat.com/sysadmin/compose-podman-pods)
