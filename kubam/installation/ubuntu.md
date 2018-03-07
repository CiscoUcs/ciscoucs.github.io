# KUBAM Ubuntu Installation

This document shows how to install KUBAM on Ubuntu 


## 1. Install Packages

```
sudo apt-get update && sudo apt-get upgrade 
sudo apt-get install docker.io
```

### Docker privileges

```
sudo usermod -aG docker $USER
```
Log out and log back in again so you can run docker as the ```ubuntu``` user. 



### Install Docker Compose
```
curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

## 2. Install Kubam

### 2.1 Test to make sure you can get docker images

Make sure you can get images from docker hub.  You can test by running: 

```
docker pull busybox
```

If the busybox image downloads fast good. Otherwise fix your docker first.

### 2.2 Docker Compose to bring up images.  

```
curl -O https://raw.githubusercontent.com/CiscoUcs/KUBaM/master/docker-compose.yml  
docker-compose up -d
```

Navigate to Port ```5000``` of this server and behold all the glory of KUBAM!

So simple!




