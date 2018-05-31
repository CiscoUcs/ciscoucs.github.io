# KUBAM Installation from source (No Docker)

For those who are appalled by the mere mention of the word "docker" we are not going to leave you hanging.  Here is how you could install it from source. 

<div class="alert alert-warning">
<b>Note</b> This is a work in progress and is still being updated.  We will hopefully simplify this as time goes on. 
</div>

### Big Picture

Before beginning let's examine what we're actually doing here.  We have two microservices that we are trying to put on the same server and make them coexist. 

The services are:

* KUBAM API - Back end Python Flask application.
* KUBAM GUI - NodeJS React application that talks to back end. 

The KUBAM API also needs to present the ```/kubam``` directory to the servers so they can mount and run. 

What we do is we front end everything with nginx.  Nginx will then have proxy ports to call either the API or the GUI depending on how it comes in.  We'll make all calls to port 80 go to the KUBAM API unless they are going to the ```/kubam``` directory, then it will go to the shared directory there.  All calls to port ```5000``` will then route to the GUI.  In this way it will work similar to how the microservices version of KUBAM works. 

So, to make everything work we do the following: 

* Install all the dependencies
* Install the source files
* Start the applications
* Start NGINX to frontend and point to the right services. 

Sounds easy right?   

## 1. Install Prerequisites

In this sample we'll use 7.3

## 1.1 Additional Repos

```
rpm -Uvh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm \
            http://ftp.tu-chemnitz.de/pub/linux/dag/redhat/el7/en/x86_64/rpmforge/RPMS/rpmforge-release-0.5.3-1.el7.rf.x86_64.rpm \
            https://forensics.cert.org/cert-forensics-tools-release-el7.rpm
```

## 1.2 YUM prereqs

```
yum -y install xorriso \
	python-jinja2 \
   PyYAML \
   fuseext2 \
   nginx \
   mkisofs \
   python-flask \
   gcc \
   python-devel \
   git \
   epel-release \
   gcc-c++ \
   make
                    		
```

## 1.3 NodeJS & Pip

### 1.3.1 PIP
Pip provides an easy way to get python modules and dependencies on our system.  We need it for the UCS APIs.

```
curl https://bootstrap.pypa.io/get-pip.py | python - && \
    pip install ucsmsdk flask_cors sshpubkeys
```

### 1.3.2 Node

NPM and Node are how we serve up front end web interfaces.

Grab the NODE repos

```
curl --silent --location https://rpm.nodesource.com/setup_8.x | sudo bash -
```

Install Node

```
yum -y install nodejs
```


## 1.4 Git KUBAM Repos

```
git clone https://github.com/CiscoUcs/KUBaM.git
git clone https://github.com/CiscoUcs/KUBAM-Frontend.git
```

## 1.5 Configure Services

```
cd KUBaM/kubam
```
Depending on which version of nginx you have it may be either:
```
cp files/default /etc/nginx.conf.d
```
or
```
cp files/default /etc/nginx/conf.d/
```
Then copy the rest of the files:

```
mkdir -p /usr/share/kubam/
cp -a files/stage1 /usr/share/kubam/stage1
cp -a templates /usr/share/kubam/
cp -a ansible /usr/share/kubam/
cp -a scripts/* /usr/bin/
```

Copy the application

```
cp -a app /
```
Edit the ```app.py``` and add this line to the first part of the file: 

```
#!/usr/bin/env python
```
Then make it executable:

```
chmod 755 /app/app.py
```

### KUBAM Web

```
mkdir -p /kubam-web
mv ~/KUBAM-Frontend/build /kubam-web/
```

## 1.6 ```kubam.yaml```

Create the KUBAM directory:

```
mkdir -p /usr/share/nginx/html/kubam
touch /kubam/kubam.yaml
```

Now we can add a basic configuration to the kubam file just to test something out. Edit ```/kubam/kubam.yaml``` and make it say something like: 

```
hosts:
- ip: 172.28.225.131
  name: kubam01
  os: centos7.3
  role: ''
```

## 1.7 Systemd

### 1.7.1 ```kubam.service```

Make Systemd init file.  Create a file called ```/etc/systemd/system/kubam.service```

Make the contents of this file be:

```
[Unit]
Description=kubam

[Service]
ExecStart=/app/app.py
```
### 1.7.2 ```kubam-web.service```
Make Systemd init file.  Create a file called ```/etc/systemd/system/kubam-web.service```

Make the contents of this file be:

```
[Unit]
Description=kubam-web

[Service]
ExecStart=serve -s /kubam-web/build --port 5002
```
### 1.7.3 Start KUBAM services


Next start up the kubam server: 

```
systemctl daemon-reload
systemctl enable kubam
systemctl enable kubam-web
systemctl start kubam
systemctl start kubam-web
```

## 1.8 Test KUBAM is up

You should be able to run ```curl localhost:5000 | python -m json.tool``` and get back an answer like: 

```
{
    "status": "ok"
}
```

At this point the API is up and running. 

Next we need to get the GUI up and running. 


## 1.9 Install GUI

```
cd ~/KUBAM-Frontend   
npm install
npm run build
npm install -g serve
serve -s build
```
             