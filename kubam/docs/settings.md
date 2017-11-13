---
layout: page
title: KUBAM Documentation: Settings
tags: Kubernetes, containers
---
{% include JB/setup %}

#Settings

The settings portion has additional information on how to configure your environment. 

## KUBAM IP address

This is the IP address of the machine where you are running docker and subsequently the kubam services.  This IP address needs to be reachable from the same network that your blades access as well as the CIMC network.  The reason for this is because:

1. The blade kickstart file has this network to access the repos for the OS install. 
2. The CIMC mounts the ISO images from this same network to perform the autmated boot installation

While it may work with DHCP relay or other methods, really the simplest way is to make the install network, the CIMC network, and the UCS management network all be on the same network.  We can always update this if required, but for now that's the way it works.  If you have an issue with that, [open an issue](https://github.com/CiscoUcs/KUBAM-Frontend/issues)

## Public Key

You'll notice that KUBAM never asks you for a password for the servers you are installing.  The reason for this is that we are trying to be more secure.  As such, we only access our KUBAM nodes using SSH keypairs.  To create SSH keypairs there is [lots of documentation](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2) on how to do this. 

When entering the public key into the SSH form, please be sure to add the ```ssh-rsa ``` portion before the key.  For example, a properly entered key would be: 

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC5QQkOU2k+zVh5gwH7AMmvF0/XsoM4R7h5xeVRQR1IBeeHjHAKoTXX04VbUD+g+9sHnsOvi+MgkHJ55EryZe7YVNI3ylfL0h1quq60Z0tFysA/6X45eJXcu5qAiLk9lkxxOrMO1x0PfVuvzJSqBA8KnPsj6F47bnM787K8x7ZfJG2nJNVZ/ZtQ+sCMcq/HSrmV6r1kY0ZmaiQWHFyR1vhY0i7h1IWVHCbXTfKMcxYfldUtiyZSMErISIcsOv2LckU6R9xOcJGYZboEkle5nrw89Pf0k+H9KXiHYG4RbldsHV1t8xbkGzZYmYXByrJd8N2+78y8HeKJyN09TpB9R9en
```
Note there should be no spaces. 

## Proxy Server

In many enterprise environments the servers are behind a firewall and don't have access to the public internet without a proxy server.  KUBAM requires the ability to reach out to docker hub and other container and package repositories to download all the necessary components.  For this we ask that you enter a proxy configuration.  If you are in an open environment you may not need a proxy environment.  The proxy server should be entered something like the following: 

```
<protocol>://<server>:<port>
```
Example:

```
http://proxy.esl.cisco.com:8080
```

IP addresses for proxy servers may not work as expected. 