# Kickstart Templates

KUBAM uses [kickstart](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/installation_guide/s1-kickstart2-file) for automated installs for RedHat and VMware ESXi.  Further supported operating systems will also use the native automated answer file for rapid installation. 

The current default kickstart templates are found in the [KUBAM source repository](https://github.com/CiscoUcs/KUBaM/tree/master/kubam/templates).  These templates are copied into the container in the ```/usr/share/kubam/templates``` directory.  

## Kickstart Templates

The kickstart template allows for a blueprint of multiple unique kickstart files for each server.  In this way every server receives its unique installation file.  This is important as each node has something unique about it including ```hostname```, ```ip address```, or different role type.  

KUBAM uses the [Jinja2](http://jinja.pocoo.org/docs/2.10/)
 framework and automiatically populates the fields based on predefined keywords.  
 
## KUBAM Template Key words

The following jinja2 variables found in a kickstart file will be automatically filled: 

* ``` {{ masterIP }} ```
* ``` \{{ netmask }} ```
* ``` {\{ gateway }} ```
* ``` {{ nameserver }} ```
* ``` {{ name }} ``` - The hostname of the server, not the FQDN.
* ``` {{ keys }} ``` - A list of public keys authorized to log into this server. 
* ```\{\{ proxy \}\}``` - A proxy server if the machine is behind a firewall.  This can be used in post scripts. 


## Workflow

The default workflow is that when a user selects __Generate Boot Images__ from the GUI the kickstart template pertaining to the OS image is filled in with all the specific nodes to be deployed.  This file is copied into a [1MB disk image](https://github.com/CiscoUcs/KUBaM/blob/master/kubam/files/stage1/ks.img)  that comes with KUBAM.  The disk image is written to the ```/kubam``` directory as the name ```<nodename>.img```.  One image is written for each node to be deployed.  This image is unique to each server. 

### Post installation

Inside each kickstart image is a series of steps to guide in post installation tasks.  For Kubernetes there is a way that looks at the different roles of a node.  If the node is a kubernetes master node, a generic node, or a kubernetes worker node, then the post installation scripts do something different. 

In the case of kubernetes nodes, it pulls a zip file found in ```~/kubam/post/``` which contains ansible instructions for deploying Kubernetes.  For generic nodes this step is omitted. 

## Customizing Kickstart Files

Most likely you will not want to use the default kickstart file as you will have ideas of how things are to be instaleld.  

To use your own template put a template file of the same name as the kubam templates in the ```~/kubam``` directory.  For example, suppose I was installing CentOS 7.4.  I would then create the file ```~/kubam/centos7.4.tmpl```.  When KUBAM goes to build the image it will see this file is in place and use it instead of the default.  

### Checking The Custom File

You are responsible for ensuring the kickstart template you provide is correct as KUBAM does no error checking.  To verify that the image you want is built, after the image is created you can check by viewing the file in the ```<nodename>.img``` image. 

For example, suppose my server that I was deploying was named ```supernode01```.  After building the deployment files, the file ```supernode01.img``` would be created in the ```~/kubam``` directory.  To view that this image uses our new custom kickstart template we would do:

```
mkdir tmp1
mount -o loop supernode01.img tmp1
```

Peaking inside the ```tmp1``` directory you will see a file called ```ks.cfg```.  You should verify that this file uses the templated file in the ```~/kubam``` directory that you used.  
 
 
