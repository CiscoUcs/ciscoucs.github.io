---
layout: page
title: KUBaM! - Stage 3 Ansible
tags: Kubernetes, containers
---

Before continuing, be sure you have completed [stage 1 and stage 2](/kubam/).  

# 1. Prerequisites

## 1.1 Get Ansible

You will need ansible installed on your build server.  This could be the same server that you are hosting the web services from.  We have tested with ```2.2.1.0```

### RedHat (YMMV)

```
yum -y install gcc python-devel
pip install ansible
```

## 1.2 Quick Check

You should already have the [KUBaM Repo](https://github.com/CiscoUcs/KUBaM) installed on your build server.  Go to the stage 3 Ansible directory:

```
cd ~/Code/KUBaM/stage3/ansible
```

## 1.3 Hosts

Put the host names in your ```/etc/hosts``` files unless you already have a DNS setup with the names.  For example, you might have something like:

```
127.0.0.1   localhost 
10.61.124.120 buildmaster
10.61.124.170 kube01
10.61.124.171 kube02
10.61.124.172 kube03
```
This has a simple 3 node kubernetes cluster.  

Next, you can put the host names in the ```~/Code/KUBaM/stage3/ansible/inventory/hosts``` file. 

You will see there is a ```master``` section and a ```nodes``` section.  If you have more nodes you can add them here. 

By default, KUBaM names the nodes ```kube0n``` where ```n``` is the node number.  The master node is ```kube01```

### 1.3.1 Verify Connectivity

```
cd ~/Code/KUBaM/stage3/ansible
ansible -m ping all 
```
This command should return that all nodes can be reached. 

If you need to set up SSH (because you didn't in the kickstart file to authorize passwordless ssh sessions from the build server) then you can modify the ```group_vars/all.yml``` to contain the proper entries to ```anisible_ssh_user``` and ```ansible_ssh_pass```.  This approach is not recommended as authorized keys is a much more efficient and secure way. 
 

You are now ready to move to [stage 4](https://ciscoucs.github.io/kubam/)

## 2.0 Customize Ansible

### 2.1 ```~/Code/KUBaM/stage3/ansible/group_vars/all.yml```

If there is no proxy set it to an empty string.  The master_ip_address should be set to the IP address of ```kube01```

The ```local_repo``` should be set to the same source where your kickstart file was specified.  

## 3.0 Run Ansible

Install Kubernetes and Contiv using:

```
cd ~/Code/KUBaM/stage3/ansible
ansible-playbook site.yml
```

This operation will take around 10 minutes and install the kubernetes cluster downloading the necessary pieces.  It uses [kubeadm](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/) and will evolve with the project as more features are supported. 

You are now ready to move to [stage 4](https://ciscoucs.github.io/kubam/)