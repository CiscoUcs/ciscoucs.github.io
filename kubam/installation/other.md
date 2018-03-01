# Other Installation Topics

## 1. No outside internet access

If you're behind a firewall and your server can't get access docker hub because your networking people are all about sweet security that's ok.  KUBAM will help you out.  You do need to at least install docker and docker compose.  Once you do that here is how you can enjoy the sweetness of KUBAM

### 1.1 Get a bastion server

On a server that can reach the internet, install docker as specified in the [standard install instructions](standard.md).  This can be done on a laptop.
  
Download the kubam files:

```
docker pull kubam/kubam
docker pull kubam/web
```

### 1.2 Save and copy files to kubam server

Now save the containers:

```
docker save -o kweb.tar kubam/web
docker save -o kubam.tar kubam/kubam
```
You'll have two files.  Upload these files to the future kubam server:

```
scp k*tar kubam:/tmp/
```
### 1.3 Restore the KUBAM containers

On the future kubam server run:

```
docker load < kubam.tar 
docker load < kweb.tar
```

Note that nodes that can't reach the internet will not be able to install kubernetes or other systems using the post install methods.  

### 1.4 Install KUBAM

Giddyup. 

Copy the [docker-compose](https://raw.githubusercontent.com/CiscoUcs/KUBaM/master/docker-compose.yml) file to the kubam server by wading through your awesome ssh bastion landmines.  Once its on the server run: 

```
cd to-the-directory-where-the-compose-file-was-copied
docker-compose up -d
```

Bam!  You are up!


