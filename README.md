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

### Nginx

```shell
podman run -d -p 8080:80 --name nginx -v $PWD/nginx:/etc/nginx/conf.d:Z nginx
```

### Tomcat

```shell

podman run -d -p 8888:8080 tomcat
```

### Flask

```shell
podman run -d -p 5000:5000 --name flask -v $PWD/python-api/app:/app:Z flask
```

## Adding container to a pod

When using a pod, use --pod <podname> and omit the port. For example

```shell
podman run -d --pod playground --name flask -v $PWD/python-api/app:/app:Z flask
```

A pod can be created with 

```shell
podman pod create --name playground
```


Find more info in this [article](https://www.redhat.com/sysadmin/compose-podman-pods)