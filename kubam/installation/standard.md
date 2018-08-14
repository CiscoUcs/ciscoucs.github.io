# KUBAM Standard Installation

This standard installation covers installing KUBAM on CentOS or RedHat.  We show how to install Docker and then KUBAM.  Do the following: 


## 1. SELinux

KUBAM supports SELinux! To check that is enabled/disabled run

```
getenforce
```

If you want it to be ```disabled``` 

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

### 1.1 Issues with SELinux

You may notice issues if you try to use symbolic links with the KUBAM directory.  

When downloading the ```docker-compose.yaml``` file in the upcoming steps you may need to modify the ```kubam``` directory to make sure that it is not using at symbolic link. If you need to use symbolic links you have two options: 

1. Change the docker-compose file to point to the real directory
2. Disable SELinux

## 2. Remove older files
We recommend Docker > 1.12.6  

If you have someting older you can install them as follows:

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

#### 3.1.1 Proxy?

Are you behind a nasty corporate firewall?  Set up the proxy in ```/etc/yum.conf```.  This is done by adding the line:

```
proxy=http://proxy.esl.cisco.com:80
```

If you were behind a Cisco firewall.  Substitute your own proxy server. 

#### 3.1.2 Install Docker
```
yum install -y yum-utils
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce
systemctl start docker
systemctl enable docker
```

#### 3.1.3 Install Docker Compose
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

## 4. Install Kubam

### 4.1 Test to make sure you can get docker images

Make sure you can get images from docker hub.  You can test by running: 

```
docker pull busybox
```

If the busybox image downloads fast go to step 4.3.  If not maybe section 4.2 can help. 

### 4.2 Proxy Service  (Only required if test in section 4.1 fails)

If you are behind a proxy and can't access docker hub by doing the test in section __4.1__ then using a proxy may be the way.  To allow Docker to use a proxy server run the following: 

```
mkdir -p /etc/systemd/system/docker.service.d
touch /etc/systemd/system/docker.service.d/https-proxy.conf
```
Edit ```https-proxy.conf``` and add proxy settings.  The below is an example of how the file should look.  Use your own proxy server in place of the Cisco proxy service. 

```
[Service]
Environment="HTTPS_PROXY=http://proxy.esl.cisco.com:80" "HTTP_PROXY=http://proxy.esl.cisco.com:80" "NO_PROXY=172.28.225.186"
```

Once this is complete run:

```
systemctl daemon-reload
systemctl enable docker
systemctl restart docker
```

Test to make sure this works: 

```
docker pull busybox
```
If it doesn't hang forever you are a happy person and can go to the next step. 

### 4.3 Docker Compose to bring up images.  

```
curl -O https://raw.githubusercontent.com/CiscoUcs/KUBaM/master/docker-compose.yml  
docker-compose up -d
```

To try version 2.0 (still under development)

```
curl -O https://raw.githubusercontent.com/CiscoUcs/KUBaM/v2.0/docker-compose.yml
```

Navigate to Port ```5000``` of this server and behold all the glory of KUBAM!




