CoreOS is a Linux distribution that is trimmed down and purpose built to run containers.  It doesn't even have its own package management system! (e.g.: no ```apt-get``` nor ```yum```) As more organizations look to build systems with Kubernetes or other Containerized solutions, using a stripped down OS can be appealing.  

In this article we will discuss how to install CoreOS on bare metal UCS.  The advantages of such an installation are the following:

* Better Performance
* Less cost.  There is no requirement to use a proprietary vendors virtualization platform.
* Less management overhead:  No need to manage a VM farm as well as a container environment.  

As with all articles in this platform it will be updated over time with new information.  

## UCS Configuration
The service profiles for a UCS blade (M3 or M4) will have the following characteristics:

* Boot from Network first, then from hard drive
* 2 x Hard Drives mirrored
* 2 x vNICs (one up A side, one up B side) These NICs do not require Fabric Failover

You'll be happy to know that CoreOS installs out of the box with no requirement for additional NIC drivers and comes right up.  While the initial deployment of a PXE server may involve some headache, once up it works great.  

If you just want to skip all this madness and use the simple latest [stable ISO image](https://stable.release.core-os.net/amd64-usr/current/coreos_production_iso_image.iso) then that is an option for you as well.  

## IPXE configuration

To make things dynamic and fast we will boot the servers from the network.  This means you will need some type of installation server that runs DHCP, TFTP, HTTP, etc.  With UCS you can put these on a seperate network and then update the vNIC after installation has completed.  

### DHCP Config
You will need to point to the files you want to install.  In our DHCP config we have the following:

```bash
#!ipxe
kernel http://${next-server}/install/coreos/coreos_production_pxe.vmlinuz coreos.config.url=http://${next-server}/install/coreos/pxe-config.ign coreos.first_boot=1
initrd http://${next-server}/install/coreos/coreos_production_pxe_image.cpio.gz
boot
```

This directs the server when it PXEboots to grab three files: 

*  ```http://${next-server}/install/coreos/coreos_production_pxe.vmlinuz``` - This is the kernel that runs the operating system.
*  ```http://${next-server}/install/coreos/pxe-config.ign``` - This is the configuration file that tells Container Linux how to install itself.  Think of this like the Kickstart file if you are familiar with RedHat system.
* ```http://${next-server}/install/coreos/coreos_production_pxe_image.cpio.gz``` - This is the RAM Disk image used to run the operating system.

All of these files use the ```${next-server}``` macro which tells the server that is booting with this file to use the IP address of the tftpserver as the address to query HTTP. 

### CoreOS binaries

Of the files that are requested, two of them are binary files that need to be downloaded from the CoreOS website.  There is also a third file that is required for the second stage of installation.  You can get these from the following commands run on your installation server in the ```/install/coreos``` directory:

```bash
wget http://stable.release.core-os.net/amd64-usr/current/coreos_production_openstack_image.img.bz2
wget http://stable.release.core-os.net/amd64-usr/current/coreos_production_pxe.vmlinuz
wget http://stable.release.core-os.net/amd64-usr/current/coreos_production_pxe_image.cpio.gz
```

### CoreOS basic configuration

Container Linux introduced a new configuration tool to configure its systems in April 2016.  This system is called [ignition](https://coreos.com/ignition/docs/0.14.0/what-is-ignition.html).  You still have the option of using cloud-config which is a simple yaml file.  In this setup we are using ignition files.  A simple ignition file to get you going would look something like the following:

```json
{
    "ignition": { "version": "2.0.0" },
    "passwd" : {
        "users" : [
            {
                "name": "vallard",
                "create" : {
                        "uid": 1000
                    },
                "passwordHash": "$1$AQGDGZZC$yGF9FviVbDZHqZiUfaZe9.",
                "sshAuthorizedKeys": [
                    "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA5xwR+1+0sBwa0wME6maFjXjIdxUS9taPOgpf1c1EJUgZENDUUOdOabDbEZ6w/xLvx7vHtYDMMTzbyKif9O5hfgQ4RXNjMIMhu+PgShfCsUCFyhMF+cKZNeg2fUZn83r9oWWcFfL31Qh8PMe3yHV30fmBUwpqdCiUCrLznefVwsIlBcnr0DaScU2TdfY73sFR69K6bBJ80GYryaQi2v2s7cjZl2sDMuv5tDNmiOZCxtDJpRS4oaILnRh0gPQaYem0Hl2AGsETsYzqbXsvKkKd96hUtKmoDQ/voHaqFvB6/don12BFQDkTtCGqOCkga7JIGWhAdZbD3+owvOPaPAvK7Q=="
                ]
            },
            {
                "name": "core",
                "sshAuthorizedKeys": [
                    "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA5xwR+1+0sBwa0wME6maFjXjIdxUS9taPOgpf1c1EJUgZENDUUOdOabDbEZ6w/xLvx7vHtYDMMTzbyKif9O5hfgQ4RXNjMIMhu+PgShfCsUCFyhMF+cKZNeg2fUZn83r9oWWcFfL31Qh8PMe3yHV30fmBUwpqdCiUCrLznefVwsIlBcnr0DaScU2TdfY73sFR69K6bBJ80GYryaQi2v2s7cjZl2sDMuv5tDNmiOZCxtDJpRS4oaILnRh0gPQaYem0Hl2AGsETsYzqbXsvKkKd96hUtKmoDQ/voHaqFvB6/don12BFQDkTtCGqOCkga7JIGWhAdZbD3+owvOPaPAvK7Q=="
                ]
            }
        ]
    }
}
```
The above file can be saved as ```/install/coreos/pxe-config.ign```.  This file will create a new user ```vallard``` with the password ```Cisco.123```.  It will also add the authorized SSH key to both the ```vallard``` user and the ```core``` user.  You should substitute your key and your own user for this if you wanted to add them.  

With all these files in place when the UCS blade boots you should be able to log into it.

## Installing to Disk

Up until now, the configuration we have created will simply boot a server with a ramdisk and kernel.  That means that nothing will persist on the server.  In fact, if you already had an Operating System installed on the disk (like Ubuntu) you could reboot and turn off the pxe server and it will simply boot back into Ubuntu.  The above is also a good starting point for installing stateless systems.  

But let's suppose that you want to have this operating system persist with reboots.  To do that there is another step and we call this __stage 1__ with __stage 0__ being the initial boot.  

Container Linux comes with a program called [```coreos-install```](https://coreos.com/os/docs/latest/installing-to-disk.html)  This progam will copy the bits of the operating system image onto disk.  In order to use it, we need to modify the ```/install/coreos/pxe-config.ign``` we created above with some intelligence to run this script.  

### Config Transpiler

When CoreOS introduced ignition there was some [grumbling on the InterWebs](https://news.ycombinator.com/item?id=11484196).  The primary complaint is that while JSON is great for machines, its not so great for humans to use.  CoreOS has a nice [tool to validate](https://coreos.com/validate) ignition files, but still maintaining them is not so great.  

One way we can get around this is by writing the files in YAML and then use the [Config Transpiler](https://github.com/coreos/container-linux-config-transpiler/blob/master/doc/getting-started.md) tool to translate from YAML to JSON.  

For an installation script we can create the following YAML file: 

```yaml
---
systemd:
  units:
    - name: installer.service
      enable: true
      contents: |
        [Unit]
        Requires=network-online.target
        After=network-online.target
        [Service]
        Type=simple
        ExecStart=/opt/installer
        [Install]
        WantedBy=multi-user.target
storage:
  files:
    - path: /opt/installer
      filesystem: root
      mode: 0500
      contents:
        inline: |
          #!/bin/bash -ex
          curl http://172.20.1.1/install/coreos/stage1.ign -o ignition.json
          coreos-install -d /dev/sda -C stable -n -b http://172.20.1.1/install/coreos -i ignition.json
          udevadm settle
          systemctl reboot
passwd:
  users:
    - name: core
      ssh_authorized_keys:
        - "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA5xwR+1+0sBwa0wME6maFjXjIdxUS9taPOgpf1c1EJUgZENDUUOdOabDbEZ6w/xLvx7vHtYDMMTzbyKif9O5hfgQ4RXNjMIMhu+PgShfCsUCFyhMF+cKZNeg2fUZn83r9oWWcFfL31Qh8PMe3yHV30fmBUwpqdCiUCrLznefVwsIlBcnr0DaScU2TdfY73sFR69K6bBJ80GYryaQi2v2s7cjZl2sDMuv5tDNmiOZCxtDJpRS4oaILnRh0gPQaYem0Hl2AGsETsYzqbXsvKkKd96hUtKmoDQ/voHaqFvB6/don12BFQDkTtCGqOCkga7JIGWhAdZbD3+owvOPaPAvK7Q=="
```
This is based off the example found in the [CoreOS Matchbox Project](https://github.com/coreos/matchbox/blob/master/examples/ignition/install-reboot.yaml)

To use this file there are further files we need to modify: 

* ```stage1.ign``` - This file is same as the previous ```/install/coreos/pxe-config.ign``` we showed above.  We have just renamed it to stage1.ign.  This file is what will be executed during the installation of Container Linux onto Disk.  It is a seperate configuration file than what we use to bootstrap the cluster.  
* ```coreos_production_image.bin.bz2``` and ```coreos_production_image.bin.bz2.sig```.  These two files are what the ```coreos-install``` script will try to get from the internet unless you download them and point it to a different installer.  These files can be downloaded from something like:
	* ```wget https://stable.release.core-os.net/amd64-usr/1298.7.0/coreos_production_image.bin.bz2```
	* ```wget https://stable.release.core-os.net/amd64-usr/1298.7.0/coreos_production_image.bin.bz2.sig```
It's important to note that Container Linux images change all the time.  So even though at the time of this writing we are using 1298.7.0 you will need to make sure that whichever stable release you use matches the files you download, or you'll need to use the ```-V``` flag on the ```coreos-install``` command.  These files will then live in ```/install/coreos/1298.7.0```
* The HTTP server in the example above is ```172.20.1.1``` and the base URL (which the ```-b``` flag signifies) will then search for the images at ```http://172.20.1.1/install/coreos/<version>/```.  You may have a different HTTP server setup so be sure the base part matches what you are serving.  

Once you are happy with this file you can transcode it with the following command:

```bash
cat install.yaml | ./ct | python -m json.tool | tee pxe-config.ign
```
where the ```ct``` command is the config transpiler binary we downloaded from [the github repo](https://github.com/coreos/container-linux-config-transpiler/releases) 

Now that you have this working you can sit back and watch the fun.  The system will reboot and you'll be able to login.  

In this article for the sake of simplicity we have used a rather trivial ignition file.  We can get more advanced and will need to if we want to install ```kubernetes``` and other systems on this server.  Expect to see more of these articles here on that subject.  

If you have any questions, please let me know on [Twitter](https://twitter.com/vallard)
