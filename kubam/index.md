---
layout: page
title: KUBAM! A Simple UCS Bare Metal Installer
tags: Kubernetes, containers
---
{% include JB/setup %}

 
![img ](img/logo.png)


You have a sweet [UCS](https://www.cisco.com/c/en/us/products/servers-unified-computing/index.html) in your datacenter, now make it dance!  

KUBAM is the fastest way to run solutions in your data center on UCS.  It takes the pain out of bare metal operating system installations and automatically provisions solutions such as Kubernetes, Docker Datacenter and other solutions.  KUBAM gives you the power to crush those who oppose you.  It is open source but enjoys a simplified experience compared to other offerings. 

## Getting Started

#### Requirements
* A KUBAM Server:  This can be a VM or Bare Metal machine that has about 20GB of disk space and a modern CPU that supports docker. Raspberry Pi?  Why not, we haven't tried it but maybe you can. 
* [Install Docker](https://www.docker.com/docker-centos-distribution).  
* [Install Docker Compose](https://docs.docker.com/compose/install/).  

#### Instructions

Log into the KUBAM server and run the following: 

```
curl -O https://raw.githubusercontent.com/CiscoUcs/KUBaM/master/docker-compose.yml 
docker-compose up -d
```
This will download two containers. We are sorry they are so large.  We are working to shrink them down.  Don't hate, give it a chance. 

Once these are up, open the IP address of the KUBAM server in a web browser on port ```5000```.  

Step through each menu, build the install images, then hit deploy.  Boom, you are done!  So fast!  So easy!

## Documentation

* [Detailed Instructions](docs/index.md) - Work in progress documentation


## Glorious Underbelly
Want to see how it works underneath?  The gory details are [here](old.md)

## Support

KUBAM only works with UCS Fabric Interconnects.  They can be blades or rack mount servers.  Why?  Cause only UCS has powerful APIs that make this easy.  

If you have problems or questions, please open an [issue](https://github.com/CiscoUcs/KUBaM/issues).  Better yet, make a pull request.  You can also [hit us up on twitter](http://twitter.com/vallard) KUBAM is scrappy, fast, changing, and brand new. 
