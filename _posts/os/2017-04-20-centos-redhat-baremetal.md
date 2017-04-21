# RedHat/CentOS Automated UCS Installation without PXE

This past week I learned about the vmedia policy that has been in UCS since the 2.2(2c).  What is great about this is it gives us a way to automate server installations without using IPXE.  

I'm a huge fan of PXE booting and I've been doing it for muchos años.  We used to use [gPXE](http://etherboot.org/wiki/index.php) and then moved on to [IPXE](http://ipxe.org/) with the rest of the industry.   In fact I still love it today.  I even wrote a lot of code in [xCAT2](https://xcat.org) that would automate this for 1200+ bare metal clusters.  

There are some things that suck about PXEbooting.  And I run into this all the time, especially in Enterprise environments.  PXEbooting requires DHCP, HTTP, TFTP, etc to all work in harmony.  And usually things just aren't set up that way.  You could make separate one off networks, but that kind of sucks.  

vMedia policies give us a way to create an autmated installation of our servers without having to mess with the network.  In this post we will outline how to use vMedia policies to create an automated environment to provision bare metal Red Hat and CentOS 7 installations.  

## 1. Prereqs

* You will need a web server on the same network or some place where the nodes that are booting can get to.  	
	* The easiest way to do this:  Suppose each node has an IP address of 192.168.2.x/24.  Then you can have a webserver on 192.168.2.2 that can have all your files. If possible make this OS the same OS that you are installing on the nodes. 

* You will need an IP address for all the servers (we are using 192.168.2.x/24.  The VLAN should already be set up for this to work in UCS and the appropriate networking.   

* Installation Media should be placed on the webserver in a place where it can be accessed.  

## 2. Create Images

We are going to create two images.  

* ISOLINUX Boot ISO Image.  This first image is the same for all nodes.  We want it as small as possible so we're not using an entire giant image for this stage clogging up our network.
* Kickstart Disk Image.  We are also creating a unique disk image for each node so that it can have its own kickstart file and thus bring uniqueness to all our nodes.  


### 2.1 Create the Boot ISO Image

__Credit:__ Some of this information was gleaned from the [help of the wonderful Internet](http://www.smorgasbork.com/2012/01/04/building-a-custom-centos-7-kickstart-disc-part-3/)

```
mkdir /tmp/kubm
mkdir -p /install/kubm
mount -o loop centos7.2.iso /tmp/kubm
cd /install/kubm
cp -a /tmp/kubm/isolinux .
cp /tmp/kubm/.discinfo isolinux/
cp /tmp/kubm/.treeinfo isolinux/
cp -a /tmp/kubm/LiveCD isolinux/
cp -a /tmp/kubm/images isolinux/
chmod 664 isolinux/isolinux.bin
```

Now edit the ```isolinux/isolinux.cfg``` file and change the first label entry to look something like the below: 

```
label linux
  menu label ^Install CentOS Linux 7
  menu default
  kernel vmlinuz
  append initrd=initrd.img inst.stage2=hd:LABEL=CentOS\x207\x20x86_64 inst.ks=hd:LABEL=KUBM:ks.cfg quiet
```
Really you should only need to change the append line and add the ```inst.ks``` line.  This will make it automatic.  You should also add the ```menu default``` line and delete it from the stanza that is below it so this comes up first. 

You could also change the time out and all kinds of other things to make it go faster and install.  

#### 2.1.1 Build the ISO Image

The build commands for the RHEL or CentOS images differ slightly in syntax.  Below are examples.  Be sure the ```-V``` flag matches what is in the isolinux.cfg file.  Note:  The isolinux.cfg file uses \x20 for spaces.  You can just use spaces below. 

##### 2.1.1.1 RedHat 7.3

```
mkisofs -o /install/redhat7.3-boot.iso -b isolinux.bin \
	-c boot.cat -no-emul-boot -V 'RHEL-7.3 Server.x86_64' \
	-boot-load-size 4 -boot-info-table -r -J -v -T isolinux/
```

##### 2.1.1.2 CentOS 7.2


```
mkisofs -o /install/centos7.2-boot.iso -b isolinux.bin \
	-c boot.cat -no-emul-boot -V 'CentOS 7 x86_64' \
	-boot-load-size 4 -boot-info-table -r -J -v -T isolinux/
```

### 2.2 Create the Kickstart Images

#### 2.2.1 Kickstart File

Creating Kickstart files is an iterative process and can be quite time consuming.  Download ```pykickstart``` so that you can validate your file is correct.

```
yum -y install pykickstart
```

The kickstart file will be unique for each node as we configure basic networking in the file and then give each node the installation media to get via http.  

##### 2.2.1.1 Basic Kickstart File
The below kickstart file will get you started.  Substitute the IP addresses for your own. 

```bash
#version=DEVEL
# System authorization information
auth --useshadow --enablemd5
# Install OS instead of upgrade
install
# Use network installation
url --url="http://192.168.2.2/install/centos7.2"
# Use graphical install
graphical
# Firewall configuration
firewall --disabled
firstboot --disable
ignoredisk --only-use=sdb,sda
# Keyboard layouts
keyboard --vckeymap=us --xlayouts='us'
# System language
lang en_US.UTF-8

# Network information
#network  --bootproto=dhcp --device=enp6s0 --ipv6=auto --activate
network --activate --bootproto=static --ip=192.168.2.213 --netmask=255.255.255.0 --gateway=192.168.2.2 --nameserver=192.168.2.2
network  --bootproto=dhcp --device=enp7s0 --onboot=off --ipv6=auto
network  --hostname=kube01
# Reboot after installation if you want.  We leave this to not reboot so we can 
# reboot
# Root password
rootpw --iscrypted $6$KVZvCsW9P.08qpM7$Yx1KnYmjxhiFcr99ocdpZYDb4MpJb6VEeZO7wrb/XRlaKfJsLkrYpy1oJLJqxbqWJQPqTAb.y.WOWV/dXjDAf0
# SELinux configuration
selinux --disabled
# System services
services --enabled="chronyd"
# System timezone
timezone US/Pacific
# System bootloader configuration
bootloader --append=" crashkernel=auto" --location=mbr --boot-drive=sda
autopart --type=lvm
# Partition clearing information
clearpart --all --initlabel

%packages
@^minimal
kexec-tools

%end


```


* __Password__ use the following to encrypt a password:  ```python -c 'import crypt,getpass;pw=getpass.getpass();print(crypt.crypt(pw) if (pw==getpass.getpass("Confirm: ")) else exit())'```

#### 2.2.2 Creating the Kickstart Image
To mount this kickstart file as a CIMC HD image we need to embed our ```ks.cfg``` file into each image.  

Using some [helpful hints from the Internet](https://thelinuxexperiment.com/create-a-virtual-hard-drive-volume-within-a-file-in-linux/) we can do this as follows: 
 
```
mkdir -p /tmp/kubm/kube01
cd /tmp/kubm/kube01
fallocate -l 1M kube01.img
dd if=/dev/zero of=kube01.img bs=1 count=1
mkfs -t ext4 kube01.img  # select y to proceed anyway
mkdir mnt
mount -o loop kube01.img mnt
cp <kickstartfile location>/ks.cfg mnt/
umount mnt
e2label kube01.img KUBM # note: This must match what was placed in the isolinux.cfg file. 
blkid kube01.img # test to see the label is there. 
```
Now copy this file to the webserver directory and test. 

### 2.3 Verify Images

You should now have a webserver that contains at the very least 3 images: 

* Kickstart images (unique per node) and named after the service profile.  So if the service profile is named ```kube01``` the image should be named ```kube01.img```
* Boot media.  One file this should be something like ```centos7.3-boot.iso``` and should be a small file. 
* Installation Media.  This is just the CentOS iso image unextracted sitting here to be installed and is referenced from your kickstart file.  

Be sure that you can ```curl``` or ```wget``` these files from the location you expect. 

# Troubleshooting

There are a ton of moving parts with this setup so it is very easy to make mistakes!  Don't worry, you are still a good person and you are still very smart.  

If boot fails it may drop you emergency shell.  From here you can see what happened. 

If you got the kickstart file successfully then you should see it in ```/etc/cmdline.d/80-kickstart.conf``` 

You should also be able to tell in the ```/run/initramfs/rdsosreport.txt```.  This can tell you information like if the kickstart file wasn't found. 

# Additional Information
This section is left as reference only but not required for making the above sections all work.  It is only here if further customizations are required, which I have found are not necessary at this point but may be in the future. 

## Modify the initrd
You probably don't need to do this but reference is here if you need to add something to the initrd.

Extract the initrd
```
xz -dc < initrd.img | cpio --quiet -i --make-directories
```

Create a non valid symbolic link in the ```/dev``` device in this directory. 

```
ln -s sr1 cdrom1
```

Pack it back up.  

```
find . 2>/dev/null | cpio --quiet -c -o | xz -9 --format=lzma >../initrd.img.new
```

Then you can place this initrd in the isolinux directory.  