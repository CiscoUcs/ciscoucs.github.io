# Windows Server 2012 R2

To install Windows using KUBAM there are a few manual steps that must be done to start.  In a high level you do the following: 

* Setup SAMBA on the KUBAM server
* Create WinPE image on existing Windows Server with UCS drivers and KUBAM custom startup files. 
* Copy WinPE ISO image to KUBAM server
* Copy Windows Server ISO image to the KUBAM server
* In the KUBAM GUI: Extract the ISO and copy template.

We'll go through each of these in detail. 
 

## 1. Setup KUBAM SAMBA server

The windows installation media is pretty big (4.3GB for Server 2012 R2).  As such, using the 1Gb CIMC link is pretty slow.  Instead we'd like to use the 40Gb links on the server.  For that to install we use the vNICs on the UCS server to connect to the KUBAM server.  But we will need to use CIFS to do this.  This is done by running the following command on the KUBAM server: 

```
docker run -d -v ~/kubam:/kubam \
           -p 139:139 -p 445:445 \
           dperson/samba \
           -s "kubam;/kubam"
```
More information on this container is available [here](https://github.com/dperson/samba)



## Windows Technician Computer Setup

Windows requires that you create an install image on an already installed [Windows Technician Computer](https://docs.microsoft.com/en-us/windows-server-essentials/install/prepare-the-technician-computer).  The Technician computer should be running the same version of Windows that you would like to install.  These instructions are for Windows Server 2012 R2 Datacenter.

The technician computer can be a virtual machine or physical machine.  If it is a physical machine it does not need to be running on Cisco hardware.

### Download Windows ADK

The Windows Assessment and Deployment Kit (ADK) is required to build WinPE images that KUBAM can use.  [Download this from Microsoft]().

Install using the default directory.

![img](../img/adk.png)

We only require the two services to be installed:

* Deployment Tools
* Windows PE

![img](../img/adk2.png)


While this installs about 3 GB, have a look at one of our [developers bee keeping websites](http://www.opg-brlekovic.hr/).  If you happen to be in Croatia you can order some honey.

### Download Cisco Drivers

The latest Cisco device drivers can be downloaded from Cisco's Support site. URLs seem to change from time to time, but was last available [here](https://software.cisco.com/download/home/283853163/type). If that link is dead, go to [https://cisco.com/support](https://cisco.com/support) and in the Downloads menu type __UCS B-Series Blade Server Software__ the main Cisco Site, then download the drivers.  It seems to be a 1GB file.  

Copy the Windows VNIC drivers to the Windows server.  Put it in the ```C:\Drivers``` directory:

```
mkdir c:\drivers
```

You should then have the VNIC drivers in this directory

```
enic6x64.cat
enic6x64.inf
enic6x64.sys
```

### Download KUBAM Windows Scripts on Technician Node

We will be creating a WinPE image that uses KUBAM and an autoattend file. To make this work we need to use the following files:

* ```winkubam.bat``` - This is the script that will create the WinPE image adding the drivers and the new ```startnet.cmd``` file. 
* ```startnet.cmd``` - This file is placed in the WinPE file and is the customized startup file we use for installing using the vMedia + the KUBAM CIFS servers. 

### Explanation of ```startnet.cmd```

```startnet.cmd``` starts up windows with the following:

* Looks in the c:\ drive to get the IP address of the machine in the file network.txt
* Mounts the KUBAM CIFS Share that has the installation media.
* Looks in the c:\ drive for the install.cmd script that does the automated installation.   

### Run ```winkubam.bat``` 

With the two prereqs in place you are ready to generate the WinPE image that will be used for the boot process. 



## Manually Creating Autoinstallation Files

UCS needs a hard drive image that includes a couple files.  This includes the 

* ```autounattend.xml``` file.  This is the template for this image to install. 
* ```network.txt``` file.  This file contains the network settings of our node and is used for starting up the server and mounting the CIFS share.   

This image can be created using: 

```
dd if=/dev/zero of=kube0${i}.img bs=1M count=1
mkfs -t fat win.img
mkdir tmpmnt
mount -o loop win.img tmpmnt
## copy files in
umount tmpmnt
rmdir tmpmnt
```