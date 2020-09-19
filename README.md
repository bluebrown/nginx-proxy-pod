# Server Setup

Example pod configuration. Nginx reverse proxy, python api, and tomcat.

## Setup

### Build the docker images

```
podman build -t flask python-api/
```

### adjust the volume mapping 

In the pod.yaml, change the path for both volumes to the path of the repoistory.

```yaml
  volumes:
  - hostPath:
      path: /home/blue/nginx-proxy-pod/nginx
      type: Directory
    name: home-blue-nginx-proxy-pod-nginx
  - hostPath:
      path: /home/blue/nginx-proxy-pod/python-api/app
      type: Directory
    name: home-blue-nginx-proxy-pod-python-api-app
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
podman run -d --pod playground --name nginx \
  -v $PWD/nginx/conf.d:/etc/nginx/conf.d:Z \
  -v $PWD/nginx/html:/usr/share/nginx/html:Z
  nginx
```

### Flask

```shell
podman run -d --pod playground --name flask \
  -v $PWD/python-api/app:/app:Z 
  flask
```

### Tomcat

```shell
podman run -d --pod playground --name tomcat \
  -v $PWD/tomcat/tomcat-users.xml:/usr/local/tomcat/conf/tomcat-users.xml:Z \
  -v $PWD/tomcat/context.xml:/usr/local/tomcat/webapps.dist/manager/META-INF/context.xml:Z \
  tomcat \
  /bin/bash -c "mv /usr/local/tomcat/webapps /usr/local/tomcat/webapps2; mv /usr/local/tomcat/webapps.dist /usr/local/tomcat/webapps; catalina.sh run"
```

## Generating a pod.yaml

```shell
podman generate kube playground >> ./pod.yaml
```

Find more info in this [article](https://www.redhat.com/sysadmin/compose-podman-pods)
