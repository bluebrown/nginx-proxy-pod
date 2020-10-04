# Deploy Docker Container with Podman 2 and Kubernetes Deployment Yaml

In this post I will recap how to set up version 2 of podman and use of of its new features,
running container from a kubernetes deployment definition file.

## Setting up Podman 2

For more details see the [offical install instructions](https://podman.io/getting-started/installation).
I will use centos for this post. 

First we need to enable the repository holding the latest release as the default repo comes currently with version 1.6 of podman.

```shell
sudo dnf -y module disable container-tools
sudo dnf -y install 'dnf-command(copr)'
sudo dnf -y copr enable rhcontainerbot/container-selinux
sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/CentOS_8/devel:kubic:libcontainers:stable.repo
sudo dnf -y install podman
```

verify the version with

```shell
podman -v
```

Next, if we want to run podman in rootless mode, we have to install [fuse-overloafs](http://rpmfind.net/linux/rpm2html/search.php?query=fuse-overlayfs)

```shell
sudo dnf -y install fuse3-devel
sudo dnf -y install fuse-overlayfs
```

to verify the installation, run the hello-world image in rootless mode.

```shell
podman run hello-world
```

## The Deployment Definition File

Before version 2 of podman it was only possible to [generate](https://www.redhat.com/sysadmin/compose-podman-pods) and use [pod](https://github.com/containers/podman/blob/master/docs/source/markdown/podman-generate-kube.1.md) definitions. But as stated in [this article](https://www.redhat.com/sysadmin/podman-play-kube), many users prefer a [deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) file.

One reason for that may be because the pod defintions as they are generated by podman look more like a data dump. Writing one from scatch feels also kubersome. It is not as well document as deployments and I have also found some features lacking I would like to use.

Now it is possible to write a deployment.yaml like below, with `podman play kube <filename>.yaml`, the same aywe would play a pod.yaml. 

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

This feels more clean and offers more features when declaring the services. Also the worry with auto generated env variables from the generated pod.yaml is gone.