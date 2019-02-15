![img](img/logo.png)

## KUBAM! is a simple UCS Bare Metal Installer.

### Why KUBAM? 

We set out with one goal: Make deploying [Kubernetes](http://kubernetes.io) on UCS simple.  But as we backtracked down the rabbit hole we found that we first needed a simple way to install Operating Systems on UCS. So while KUBAM works well installing Kubernetes, it also works well installing other operating systems:

* VMware ESXi 6.0, 6.5, 6.7
* RedHat/CentOS 7.2 - 7.5
* Ubuntu 18.04
* Windows 2012 R2, 2018 

Other operating systems can be added pretty quickly.  Just [let us know on twitter](https://twitter.com/vallard)

But, why KUBAM? Most legacy solutions install bare metal using PXE.  PXE works well but is complicated: It requires MAC address mapping, DHCP, TFTP, etc. It also has security issues which make it not something that can always be placed in a production network. 

KUBAM uses UCS vMedia policies to install operating systems.  You can learn more about that in a [blog post](../OS/REDHAT.md) that we wrote. KUBAM simply automates this process. 

Using the UCS APIs simplifies the installation, makes it more secure, and eliminates complications.  

KUBAM is the fastest way to run solutions in your data center on UCS. It takes the pain out of bare metal operating system installations and automatically provisions solutions such as Kubernetes, Docker Enterprise, VMware ESXi clusters, general Linux servers and other solutions. 

KUBAM gives you the power to crush those who oppose you. It is open source but enjoys a simplified experience compared to other offerings.

