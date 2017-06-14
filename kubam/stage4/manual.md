---
layout: page
title: KUBaM! - Stage 4 Manual
tags: Kubernetes, containers
---

Before continuing, be sure you have completed [stage 1 - stage 3](/kubam/).  

At this point your Kubernetes cluster is installed.  We will run a few scripts to ensure that you can now start doing work on your cluster.

# 1. Verify up

Log into ```kube01``` and verify you are up and running:

```
ssh kube01
kubectl get componentstatuses
```
You should see etcd healthy. 

```
kubectl get nodes
```
You should see three nodes up

```
NAME      STATUS         AGE
kube01    Ready,master   26m
kube02    Ready          23m
kube03    Ready          23m
``` 

# 2. Kubectl

You may decide you want to access your cluster remotely.  This requires the ```kubectl``` command tool to be installed on the machine you want to access from as well as creating a file on your build server (or MacOS) and set ```kubectl``` to use it.  

## 2.1 Get kubectl

Instructions are [posted here](https://kubernetes.io/docs/tasks/tools/install-kubectl/).  We recommend version 1.5.4 as this is the version that works with contiv.

```
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.5.4/bin/linux/amd64/kubectl
chmod 755 kubectl
sudo mv kubectl /usr/local/bin
```

## 2.2 Config Kubectl


You create a file called:

```
~/.kubectl/config
```

Most of the contents of the file can be retrieved from ```kube01``` in ```/etc/kubernetes/admin.conf```
To make it simple just run the following: 

```
mkdir -p ~/.kube
scp kube01:/etc/kubernetes/admin.conf ~/.kube/config
```
After doing this, ```kubectl``` should work right away:

```
kubectl get componentstatus
```

## 2.1 troubleshooting

If you are using proxies, make sure that you have the kubernetes master node configured in your ```~/.bash_profile``` as ```no_proxy```, example: 

```
export no_proxy=10.61.124.100,10.61.124.170
```
 
In the above example, this is set with the build server IP address and the kube01 IP address. 

