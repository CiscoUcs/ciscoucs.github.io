---
layout: page
title: KUBAM Documentation: KUBAM node
tags: Kubernetes, containers
---
{% include JB/setup %}

# KUBAM Node

KUBAM has been tested with CentOS and others.  To get started you will need a node with about 20GB of hard drive space . 


## 1. Disable SELinux

We don't support this and the docker containers will have issues if you have SELinux enabled.  To see if it is run:

```
getenforce
```

If it is, you need to get rid of it. 

Edit ```/etc/sysconfig/selinux``` and set the file to look like:

```

# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=disabled
# SELINUXTYPE= can take one of three two values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected.
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted
```
Notice that ```SELINUX=disabled``` is set.  Once this is done you need to reboot the node!

## 2. Remove older files
We like to use the latest docker binaries.  Please remove the older ones that may be packaged with the operating system. 

#### CentOS 7
```
yum remove docker \
           docker-common \
           docker-selinux \
           docker-engine
```

## 3. Install Docker and Docker Compose

### 3.1 CentOS 7

Run the following commands as ```root```.  Run ```sudo``` before if necessary:

#### 3.1.1 Install Docker
```
yum install -y yum-utils
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce
systemctl start docker
systemctl enable docker
```

#### 3.1.2 Install Docker Compose
```
curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 3.2 RedHat 7

Behind a proxy?  Run:

```
export https_proxy=proxy.esl.cisco.com:80
export http_proxy=proxy.esl.cisco.com:80
```
substitute your proxy for the cisco one shown in the example above. 

#### 3.2.1 RHN

Register your server

```
subscription-manager register
subscription-manager subscribe
```

Are you Behind a proxy? Run the following:

```
subscription-manager config --server.proxy_hostname=proxy.esl.cisco.com --server.proxy_port=80
```

(Substitute your proxy server)

Subscribe to rhel extras

```
subscription-manager repos --list
subscription-manager repos --enable rhel-7-server-extras-rpms
subscription-manager repos --enable=rhel-7-server-optional-rpms
```

(That command takes like 5 million years to return cause RHN is the slowest turd ever. Hello, am I talking to a 1997 web service? Also, its been slow like this since from forever.  Hopefully you have a satellite)

#### 3.2.2 Install Docker

```
yum -y install docker
systemctl enable docker
systemctl start docker
```

#### 3.2.3 Install Docker Compose
```
curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```
Alternatively you can use the EPEL repo

```
curl -O https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum -y install ./epel-release-latest-7.noarch.rpm
yum -y install docker-compose
```

### 4. Install Kubam

```
curl -O https://raw.githubusercontent.com/CiscoUcs/KUBaM/master/docker-compose.yml  
docker-compose up -d
```

Navigate to Port ```5000``` of this server and behold all the glory of KUBAM!

## 5. No Internet access Installation

If you're behind a firewall and your server can't get access docker hub because your networking people are all about sweet security that's ok.  KUBAM will help you out.  You do need to at least install docker and docker compose.  Once you do that here is how you can enjoy the sweetness of KUBAM

### 5.1 Get a bastion server

On this server install docker as specified above.  
Download the kubam files:

```
docker pull kubam/kubam
docker pull kubam/web
```

### 5.2 Save and copy files to kubam server

Now save the containers:

```
docker save -o kweb.tar kubam/web
docker save -o kubam.tar kubam/kubam
```
You'll have two files.  Upload these files to the future kubam server:

```
scp k*tar kubam:/tmp/
```
### 5.3 Restore the KUBAM containers

On the future kubam server run:

```
docker load < kubam.tar 
docker load < kweb.tar
```

Note that nodes that can't reach the internet will not be able to install kubernetes or other systems using the post install methods.  

### 5.4 Install KUBAM

Giddyup. 

Copy the [docker-compose](https://raw.githubusercontent.com/CiscoUcs/KUBaM/master/docker-compose.yml) file to the kubam server by wading through your awesome ssh bastion landmines.  Once its on the server run: 

```
cd to-the-directory-where-the-compose-file-was-copied
docker-compose up -d
```

Bam!  You are up!





