---
layout: page
title: KUBAM! Advanced Connections
tags: Kubernetes, containers
---
{% include JB/setup %}

This document presents several cases where you may want to customize KUBAM to meet whatever datacenter needs you may have. 

## Special Kernel parameters

Adding kernel parameters to the boot ISO image allows the server to boot in a specific way.  Let's suppose you wanted to modify the kernel parameters of the RedHat 7.2 ISO image. 

Run KUBAM as normal and press the __Make ISO Images__ button in the deploy tab.  Before you press the __Deploy__ button do the following: 

```
cd ~/kubam
mkdir -p mnt
mount -o loop redhat7.2-boot.iso mnt
cd mnt
vi isolinux.cfg
```

Modify the ```isolinux.cfg``` file by adding the kernel parameters.  For example: 

```diff
- append initrd=initrd.img inst.stage2=hd:LABEL=RHEL-7.2\x20Server.x86_64 inst.ks=hd:LABEL=KUBAM:ks.cfg quiet
+ append initrd=initrd.img inst.stage2=hd:LABEL=RHEL-7.2\x20Server.x86_64 inst.ks=hd:LABEL=KUBAM:ks.cfg net.ifnames=0 biosdevname=0 quiet

```