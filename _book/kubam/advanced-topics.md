This document presents several cases where you may want to customize KUBAM to meet whatever datacenter needs you may have. 

## Custom Kickstart Files
If you don't want to use the provided KUBAM kickstart file you can use your own.  Start from the kubam examples and configure from there. To get the custom kubam file, you can do the following:

```
cd ~/kubam
```
Grab a [sample template](https://github.com/CiscoUcs/KUBaM/tree/master/kubam/templates) from the kubam repo. Example: 

```
curl -O https://raw.githubusercontent.com/CiscoUcs/KUBaM/master/kubam/templates/centos7.4.tmpl 
```

Make sure it is named the expected OS name like they appear in the kubam repo or it will not grab your file. 

Run the __Make ISO Images__ in the deploy tab on KUBAM. 

## Special Kernel parameters

Adding kernel parameters to the boot ISO image allows the server to boot in a specific way.  Let's suppose you wanted to modify the kernel parameters of the RedHat 7.2 ISO image. 

Run KUBAM as normal and press the __Make ISO Images__ button in the deploy tab.  Before you press the __Deploy__ button do the following: 

```
cd ~/kubam
rm -rf redhat7.2-boot.iso 
```

log into the kubam/kubam container: 

```
docker exec -it $(docker ps | grep kubam/kubam | awk '{print $1}') /bin/bash
```

This will put you in the container.  From here edit

```
/usr/share/kubam/stage1/redhat7.2/isolinux.cfg
```

Add the desired kernel parameters.  For example: 

```diff
- append initrd=initrd.img inst.stage2=hd:LABEL=RHEL-7.2\x20Server.x86_64 inst.ks=hd:LABEL=KUBAM:ks.cfg quiet
+ append initrd=initrd.img inst.stage2=hd:LABEL=RHEL-7.2\x20Server.x86_64 inst.ks=hd:LABEL=KUBAM:ks.cfg net.ifnames=0 biosdevname=0 quiet

```

Make sure you don't append IP addresses as this image is used by all nodes that will boot this OS.  Therefore it needs to be generic.  The IP addresses are configured in the kickstart file template. 
