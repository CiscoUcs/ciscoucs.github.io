# Ubuntu vMedia Installation

__Date:__ Feb 2019 __Author:__ [@vallard](https://twitter.com/vallard)

This tutorial will explain how to install Ubuntu on UCS bare metal using vMedia policies to create an automated installation.  This is the method used by KUBAM to deploy Ubuntu on Bare Metal. 

## 1. Get base OS image media

You can get the Ubuntu 18.04 image from the alternative downloads.  If you get the standard live server this method won't work.  Here is a [link that works today](http://cdimage.ubuntu.com/releases/18.04.1/release/ubuntu-18.04.1-server-amd64.iso).  

## 2. Build Boot ISO Image

Mount the Ubuntu ISO image.  This could be done with: 

```
sudo mkdir -p /root/kubam/ubuntu18.04
sudo mount -o loop <ubuntu iso>.iso /media
sudo cp -rT /media/ /root/kubam/ubuntu18.04
export BASEPATH=/root/kubam/ubuntu18.04
```

Now create the directory where our boot files will go:

```
sudo mkdir ubuntu18.04-boot
```

Now copy the following files from the base media to the boot dir.  We try to keep it small so we only copy what we need:

```
export BASEPATH=/root/kubam/ubuntu18.04
cd ubuntu18.04-boot
cp $BASEPATH/isolinux/f*txt . 
cp $BASEPATH/isolinux/splash.png . 
cp $BASEPATH/isolinux/vesamenu.c32 . 
cp $BASEPATH/isolinux/txt.cfg .
cp $BASEPATH/isolinux/stdmenu.cfg .  
cp $BASEPATH/isolinux/rqtxt.cfg . 
cp $BASEPATH/isolinux/prompt.cfg . 
cp $BASEPATH/isolinux/menu.cfg . 
cp $BASEPATH/isolinux/libutil.c32 .
cp $BASEPATH/isolinux/libcom32.c32 .
cp $BASEPATH/isolinux/ldlinux.c32 .
cp $BASEPATH/isolinux/isolinux.cfg .
cp $BASEPATH/isolinux/isolinux.bin . 
cp $BASEPATH/isolinux/exithelp.cfg .
cp $BASEPATH/isolinux/boot.cat .
cp $BASEPATH/isolinux/adtxt.cfg .
cp $BASEPATH/install/netboot/ubuntu-installer/amd64/linux . 
cp $BASEPATH/install/netboot/ubuntu-installer/amd64/initrd.gz .
cp -a $BASEPATH/boot .
cp $BASEPATH/preseed/ubuntu-server-minimal.seed . 
```

Now we'll need to edit a few files in this directory: 

### 2.2 Edit `isolinux.cfg`

Remove the last line and set the timeout to 3.

```
# D-I config version 2.0
# search path for the c32 support libraries (libcom32, libutil etc.)
path
include menu.cfg
default vesamenu.c32
prompt 1
timeout 3
```
This way it starts in 3 microseconds and you don't have to wait for anything. If you want it to wait longer before installing you can put different timeout values. 


### 2.3 Edit `txt.cfg`


We edit the `txt.cfg` file to look as follows:

```
default install
label install
  menu label ^Install Ubuntu Server
  kernel linux
  append netcfg/disable_autoconfig=true netcfg/confirm_static=true netcfg/get_ipaddress=192.168.1.42 netcfg/get_netmask=255.255.255.0 netcfg/get_nameservers=192.168.1.1 netcfg/get_gateway=192.168.1.1 url=http://192.168.1.14/kubam/preseed.cfg initrd=initrd.gz hostname=kubam01 domain=local mirror/http/hostname=192.168.1.14 mirror/country=manual mirror/http/proxy= protocol=http mirror/http/directory=/kubam/ubuntu18.04 keymap=us locale=en_US --- DEBCONF_DEBUG=5

label hd
  menu label ^Boot from first hard disk
  localboot 0x80
  
```

As you can see there is a lot of static part of the configuration that we put into the kernel command line.  The gist of it is that we define the network and some other necessary parameters so that it can automatically start the installation.  It then grabs the rest of the parameters from the `preseed` file that lives on the server.  

The bulk of the details of the `preseed` file is [documented here](https://help.ubuntu.com/lts/installation-guide/amd64/apbs04.html). We will break down the kernel parameters we use here:

* `netcfg/disable_autoconfig=true` - If this is not set the server will attempt do install via DHCP.  We prefer to set it static. 
* `netcfg/confirm_static=true` - If we don't put this it asks if we really really want to do a static IP.  Yes we do. 
* `etcfg/get_ipaddress=192.168.1.42`, `netcfg/get_netmask=255.255.255.0`,  `netcfg/get_nameservers=192.168.1.1`, `netcfg/get_gateway=192.168.1.1` - Here we are setting the static IP address of the server.  If any of these parameters are left out it will prompt us for answers. We don't want that to happen :-)
* `url=http://192.168.1.14/kubam/preseed.cfg` - This is the preseed config file that is used for the node.  It has extra details in it.  This file lives on the server `192.168.1.14` in the specified directory.  During the install, the host will reach out to the `192.168.1.14` server and try to read this file. 
* `hostname=kubam01`, `domain=local` - Local hostname configuration for the server.  
* `initrd=initrd.gz` - The ramdisk that will be used to boot the machine.  This file is in the customized CD image we make. 
* `mirror/http/hostname=192.168.1.14`,  `mirror/country=manual mirror/http/proxy=`, `protocol=http`, `mirror/http/directory=/kubam/ubuntu18.04` - These settings are so that we download the Ubuntu files directly from the server as opposed to going out to the internet to fetch them.  This helps us install in air gapped environments.  Since the boot ISO image is only 50MB all the packages live elsewhere. 
* `keymap=us`, `locale=en_US` - Used to set locale. Otherwise we would be prompted. 
* `DEBCONF_DEBUG=5` - Adding this kernel parameter lets us get more logs of the install process on `Alt-F4`.  It helps debug.  You can leave it off. 

Many of these details should be put in just the preseed file, the issue is the installer still stops unless we have some of these on the command line.  

### 2.4 Make the Boot ISO image.

To make the boot ISO image we run:

```
apt install genisoimage
mkisofs -D -r -V "UBUNTU" -cache-inodes -J -l -b isolinux.bin -c boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -o ubuntu18.04-boot.iso ubuntu18.04-boot/
```

We now have a boot ISO image we can use with a Vmedia image for one node.  But we will still need to create the `preseed` file and put it on our server. 

## 3. Make the preseed file

Our file looks as follows:

```
d-i debconf/priority string critical
d-i auto-install/enable boolean true
d-i anna/choose_modules apt-cdrom-setup

# use -proposed udebs
d-i apt-setup/proposed boolean false

# minimal install (the only one not working!)
ubiquity ubiquity/minimal_install boolean true

# localization
d-i debian-installer/language string en
d-i debian-installer/country string US
d-i debian-installer/locale string en_US.UTF-8

# keyboard
d-i console-setup/ask_detect boolean false
d-i keyboard-configuration/xkb-keymap select us

# use static network configuration
d-i netcfg/get_hostname string unassigned-hostname
d-i netcfg/get_domain string unassigned-domain
d-i netcfg/disable_autoconfig boolean true
d-i netcfg/choose_interface select enp0s3
d-i netcfg/get_ipaddress string 192.168.1.42
d-i netcfg/get_netmask string 255.255.255.0
d-i netcfg/get_gateway string 192.168.1.1
d-i netcfg/get_nameservers string 192.168.1.1
d-i netcfg/confirm_static boolean true


# user setup
d-i passwd/user-fullname string kubam
d-i passwd/username string kubam
d-i passwd/user-password password Cisco.123
d-i passwd/user-password-again password Cisco.123
d-i user-setup/allow-password-weak boolean true
d-i user-setup/encrypt-home boolean false

# enable shadow passwords
d-i passwd/shadow boolean true

# Date/Time settings
d-i clock-setup/utc boolean true
d-i time/zone string US/Pacific
d-i clock-setup/ntp boolean true


# release to install
d-i mirror/suite string bionic

# do not enable live installer, use normal instead
d-i live-installer/enable boolean false

# auto-partition, all files in one partition
# if there is only one disk this works: 
#d-i partman-auto/init_automatically_partition select biggest_free
#d-i partman-auto/method string regular
#d-i partman-auto/choose_recipe select atomic
#d-i partman/choose_partition select finish
#d-i partman/confirm_nooverwrite boolean true
#d-i partman/confirm boolean true

# auto partition if there are multiple disks. 
# Here we choose /dev/sdd as the disk to install on. 
d-i partman-auto/method string regular
d-i partman-auto/disk string /dev/sdd
d-i partman-lvm/device_remove_lvm boolean true
d-i partman-auto/choose_recipe select atomic
d-i grub-installer/bootdev string default
d-i partman-partitioning/confirm_write_new_label boolean true
d-i partman/choose_partition select finish
d-i partman/confirm boolean true
d-i partman/confirm_nooverwrite boolean true

# reboot at the end
d-i finish-install/reboot_in_progress note

```
There are many more complicated setups you could use but this is one that gets our systems up and running. 

Now for each host to be installed you need to put a `preseed.cfg` on a server that each host can reach during the installation. 

## 4. Setup Vmedia Policy

The best strategy would be to create a unique ISO image for each host and name the ISO after the UCS Service Profile Name.  This way each server would grab this ISO file and boot it up.  Then each server would have its own preseed file it could access as well.  If this sounds tedious using any configuration management tool could actually set this up.  We use [kubam](https://kubam.io) to do this for us as it also serves the files. 

By using this we now can boot the server and the OS comes up automatically! 

Hit me up if there are any questions on [@twitter](https://twitter.com/vallard). 