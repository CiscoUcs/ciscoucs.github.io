# KUBAM Installation from source (No Docker)

For those who are appalled by the mere mention of the word "docker" we are not going to leave you hanging.  Here is how you could install it from source. 

<div class="alert alert-warning">
<b>Note</b> This is a work in progress and is still being updated.  We will hopefully simplify this as time goes on. 
</div>
 

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
   git
                    		
```

## 1.3 Pip and Pip packages

```
curl https://bootstrap.pypa.io/get-pip.py | python - && \
    pip install ucsmsdk flask_cors sshpubkeys
```

## 1.4 Git KUBAM Repos

```
git clone https://github.com/CiscoUcs/KUBaM.git
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
cp files/nginx.conf /etc/nginx/nginx.conf
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

## 1.6 ```kubam.yaml```

Create the KUBAM directory:

```
mkdir -p /kubam
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

Make Systemd init file.  Create a file called ```/etc/systemd/system/kubam.service```

Make the contents of this file be:

```
[Unit]
Description=kubam

[Service]
ExecStart=/usr/bin/init.sh
```

Next start up the kubam server: 

```
systemctl daemon-reload
systemctl enable kubam
systemctl start kubam
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


                   