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

You may decide you want to access your cluster remotely.  This requires you to create a file on your build server (or MacOS) and set ```kubectl``` to use it.  You create a file called:

```
~/.kubectl/config
```

Most of the contents of the file can be retrieved from ```kube01``` in ```/etc/kubernetes/admin.conf```
To make it simple we have an example that looks as follows: 

```
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: <long-key>
    server: https://10.61.124.170:6443
  name: ams
contexts:
- context:
    cluster: ams
    user: admin
  name: default-context
current-context: default-context
kind: Config
preferences: {}
users:
- name: admin
  user:
    user:
    client-certificate-data: <long-key>
    client-key-data: <long-key> 
```


The values for the keys are found on ```kube01``` in ```/etc/kubernetes/admin.conf```

The value for the server is the IP address of ```kube01```

Once you have this file you set kubectl to use the default context you created:

```
kubectl config use-context default-context
```

## 2.1 troubleshooting

If you are using proxies, make sure that you have the kubernetes master node configured in your ```~/.bash_profile``` as ```no_proxy```, example: 

```
export no_proxy=10.61.124.100,10.61.124.170
```
 
In the above example, this is set with the build server IP address and the kube01 IP address. 

