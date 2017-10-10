---
layout: page
title: KUBaM! - Stage 1 - Docker Image
tags: Kubernetes, containers
---

To simplify bare metal UCS configurations KUBaM provides a container image that can be run to create a web server to create resources required for bare metal installations. These resources include media source as well as automated boot files. 

The advantage of UCS is that a PXE server is not required to do automated Kickstart Installations.  Thus we can achieve rapid provisioning with less complication using the advanced API that UCS provides for us.  

The container image simply automates the manual steps shown in the [manual settings](https://ciscoucs.github.io/kubam/stage1/manual) instructions.  

 
# 1. Provision an Installation Server

An installation server can be created with a VM or another bare metal server.  The installation server has the following requirements:

* Should be on the same network as the nodes that will be provisioned.  It may work on a different network but it will simplify your life if you keep it on the same network. 
* Should ahve at least 40GB of disk space.  This is for the media that you want to provision.  The truth is the Docker image is less than 300MB and the Installation Media will only take about 2GB.  But disk space is cheap and your time is not, so go big if you can.  But 40GB minimum.  
* We will use CentOS for our server but really any server that can run docker should work.  
* Ensure there is no other web server running on this server. 
* SELinux will just cause problems and we don't currently support it.  If running CentOS ensure to run ```setenforce 0``` or edit ```/etc/sysconfig/selinux``` and set ```SELINUX=disabled``` and reboot. 
* Ensure IP forwarding is enabled (RedHat/CentOS).  This can be done with ```echo net.ipv4.ip_forward = 1 >>/etc/sysctl.d/99-sysctl.conf```

## 1.1. Install Docker and Wget 

For CentOS this can be done as follows: 

```
yum -y install docker wget
systemctl enable docker
systemctl start docker
```

### 1.1.1 Proxy (Do this only if the Install Server requires a proxy)
If you are behind a proxy, then you will need to make some changes:

```
https_proxy=proxy.esl.cisco.com:80 yum -y install docker
mkdir -p /etc/systemd/system/docker.service.d
touch /etc/systemd/system/docker.service.d/https-proxy.conf
```
Edit the ```https-proxy.conf``` so it can reach proxy.  It should look something like the following: 
```
[Service]
Environment="HTTPS_PROXY=http://proxy.esl.cisco.com:80" "HTTP_PROXY=http://proxy.esl.cisco.com:80" "NO_PROXY=172.28.225.186"
```

Once this is complete: 

```
systemctl daemon-reload
systemctl enable docker
systemctl restart docker
```

# 2. Obtain Installation Media

For Kubam we want a directory that will contain our installation media and that will be used by the docker container as a permament volume.  This diretory can be anywhere.  We will assume it is in ```~/kubam```.  

```
mkdir -p ~/kubam
cd ~/kubam
```

Now download the latest Minimal CentOS 7 image.  This can be done by running something like: 

```
wget http://mirrors.ocf.berkeley.edu/centos/7/isos/x86_64/CentOS-7-x86_64-Minimal-1611.iso
```

For other mirros, [check this page.](http://isoredirect.centos.org/centos/7/isos/x86_64/CentOS-7-x86_64-Minimal-1611.iso)

You should now have a directory with a 680MB file named something like ```CentOS-7-x86_64-Minimal-1611.iso```


# 3. Create Configuration File

KUBaM stage 1 uses a simple configuration file to automatically tell it how to load.  This file can be copied from [the Github Source](https://github.com/CiscoUcs/KUBaM/blob/master/stage1/stage1.yaml)

Edit this file and place it in the ```~/kubam``` directory.  It should be called ```stage1.yaml```.  

E.g:
```
cd ~/kubam
wget https://raw.githubusercontent.com/CiscoUcs/KUBaM/master/stage1/stage1.yaml
```
(Use proxy if necessary)

## 3.1 Editing Tips

* ```masterIP``` - You should place the IP address of your installation server.  This is the IP address of the server this file is on right now.  
* ```public_keys``` - KUBaM doesn't allow for passwords.  In order to log into your servers you will need a Public Key.  Place a list of public keys.  See [This Example](https://www.cyberciti.biz/faq/linux-generating-rsa-keys/) if this is new to you.  The id_rsa.pub is the output that should be added to these lines.  You can have more than one, but one is probably all you need to get started.  Ensure the public key of this server is on it. 
* ```nodes``` - Each node should have a name and an IP address.  Further stages in KUBaM dictate that the nodes be named ```kube0x``` where x : {1, 2,...}.  For clusters bigger than 9, be sure to remove the zero:  e.g.: ```kube10```.  Add or delete nodes so you have what is appropriate for your cluster.  We recommend 3 as the minimum. 
* ```network``` - These fields are required.  You must have the netmask, gateway, and nameserver defined for your nodes.  These paramaters are common for each node. 

# 4. Run KUBaM Stage1 container

If everything is set right, you should now have a directory with two files: 

* CentOS ISO image
* ```stage1.yaml``` file customized

From here you can now run: 

```
cd ~/kubam
docker run -p 80:80 -d -v `pwd`:/kubam \
	--device /dev/fuse \
	--cap-add SYS_ADMIN \
	--name kube-stage1 \
	kubam/stage1-server
```
This could take several minutes to download the docker image and setup.  

# 5. Verification and Troubleshooting

If all is well, you should now be able to navigate to http://<masterIP>/kubam

This page will show a diretory listing of the iso file as well as *.img files for each of the nodes.  
You are now ready to go on to the [next stage](http://kubam.io)

## 5.1 Troubleshooting

If you are unable to reach the web server, check that the container is running:

```
docker ps
```
If the container is not running there may have been an issue starting it.  You can then examine the log files. 

To get this run:

```
docker ps -a
```
You should see the poor dead container there.  To examine the logs, do: 

```
docker logs kube-stage1
```

If you see a bunch of permission denied errors it may be that SELinux is enforcing.  Delete the container: 

```
docker rm kube-stage1
setenforce 0
```
Then rerun the container command described above in section 4. 


	

