![img](img/logo.png)

## KUBAM! is a simple UCS Bare Metal Installer.

### Why KUBAM? 

We set out with one goal: Make deploying [Kubernetes](http://kubernetes.io) on UCS simple.  But as we backtracked down the rabbit hole we found that we first needed a simple way to install Operating Systems on UCS.

Most legacy solutions install bare metal using PXE.  PXE works well but is complicated: It requires MAC address mapping, DHCP, TFTP, etc. It also has security issues which make it not something that can always be placed in a production network. 

KUBAM uses UCS vMedia policies to install operating systems.  You can learn more about that in a [blog post](../OS/REDHAT.md) that we wrote. KUBAM simply automates this process. 

Using the UCS APIs simplifies the installation, makes it more secure, and eliminates complications.  

KUBAM is the fastest way to run solutions in your data center on UCS. It takes the pain out of bare metal operating system installations and automatically provisions solutions such as Kubernetes, Docker Enterprise, VMware ESXi clusters, general Linux servers and other solutions. 

KUBAM gives you the power to crush those who oppose you. It is open source but enjoys a simplified experience compared to other offerings.

