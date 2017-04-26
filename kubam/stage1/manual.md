---
layout: page
title: KUBaM! - Stage 1 Manual Setup
tags: Kubernetes, containers
---

For the UCS Bare Metal setup KUBaM uses vMedia Policies to do the automated installation.  This requires the following prereqs: 

* UCS Manager 2.2(2c) or higher.  (Preferably higher... come on!  Update your UCS!)
* B200 M3 or C2XX M3 servers or higher.  Servers below these models don't allow vMedia policies. 
* One Master Server that has access to UCSM and the Kubernetes Network.  It works easiest if the Master Server is on the same subnet of the kubernetes nodes, but this is not a requirement as long as 

# 1. Setup Web Server

## 1.1 nginx on CentOS/RedHat 7

```bash
yum -y install nginx
systemctl start nginx
```

Open the firewall if ```firewalld``` is running:

```
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --reload
```
__Note:__ this assumes that ```firewall-cmd --get-active-zones``` showed the ```public``` zone was running. 

The root of the webpages defaults to serve from ```/user/share/nginx/html```.  We will put all the ISO files in this directory. 

### 1.1.1 Optional: Allow directory listing

By default, nginx doesn't allow the user to see the files in the root directory.  If you get rid of the ```index.html``` file you will then see a __403 Forbidden__ error when you try to access the webpage. 

To change this behavior you can modify the ```/etc/nginx/nginx.conf``` file.  After the lines: 

```
location / {
}
```

Adding the following: 

```
location /kubam {
  autoindex on;
}
```

Then run: 

```
mkdir /usr/share/nginx/html/kubam
systemctl nginx restart
```

We can now put all of our files in the ```/usr/share/nginx/html/kubam``` directory and see a listing of all of them when we navigate to ```http://example.com/kubam/```. 


# 2. Prepare Boot ISO Media

For more information on this process [see this post](http://localhost:4000/os/2017/04/20/centos-redhat-baremetal) 

The working directory is the html directory of your webserver.  Assume for this example it is ```/usr/share/nginx/html/kubam/```

```
export WORKDIR=/usr/share/nginx/html/kubam
cd $WORKDIR
```
The ISO image for the OS we will install should be in this directory. 

```
mkdir -p mnt stage1
mount -o loop rhel-server-7.3-x86_64-dvd.iso mnt
cp -a mnt/isolinux/ stage1/
cp mnt/.discinfo stage1/isolinux
cp -a mnt/LiveOS stage1/isolinux/
cp -a mnt/images/ stage1/isolinux/
umount mnt
```

Edit the ```stage1/isolinux/isolinux.cfg``` file: 

```diff
label linux
  menu label ^Install Red Hat Enterprise Linux 7.3
+ kernel vmlinuz
  menu default
+ append initrd=initrd.img inst.stage2=hd:LABEL=RHEL-7.3\x20Server.x86_64 inst.ks=hd:LABEL=KUBAM:ks.cfg quiet
- append initrd=initrd.img inst.stage2=hd:LABEL=RHEL-7.3\x20Server.x86_64 quiet

label check
  menu label Test this ^media & install Red Hat Enterprise Linux 7.3
  kernel vmlinuz
- menu default
  append initrd=initrd.img inst.stage2=hd:LABEL=RHEL-7.3\x20Server.x86_64 rd.live.check quiet
```
Now Pack up the ISO boot image: 

```
yum -y install mkisofs
mkisofs -o $WORKDIR/rh73-boot.iso -b isolinux.bin \
	-c boot.cat -no-emul-boot -V 'RHEL-7.3 Server.x86_64' \
	-boot-load-size 4 -boot-info-table -r -J -v -T stage1/isolinux
```
Tragically, this is a 497MB image.  😰



# 3. Prepare Install Tree

Create a directory with the OS name and copy the contents of the OS ISO to this directory: 

```
mkdir rh7.3
mount -o loop rhel-server-7.3-x86_64-dvd.iso mnt
cp -a mnt/* rh7.3/
cp mnt/.discinfo rh7.3/
cp mnt/.treeinfo rh7.3/
umount mnt
```

# 4. Prepare Kickstart Images
Kickstart Images are used for individual nodes.  Each image should be named after the service profile (SP) name of the server.  If there are spaces in the SP name then they should be given dashes instead of spaces for the name. 

```bash
for i in $(seq -w 1 3) 
do 
	fallocate -l 1M kube0$i.img
	dd if=/dev/zero of=kube01.img bs=1 count=1
	mkfs -t ext2 kube0$i.img
	e2label kube0$i.img KUBAM
	mkdir $WORKDIR/kube0$i/
	mount -o loop kube0$i.img kube0$i
done
```
<div class="alert alert-warning">
<b>Note:</b> When running this script it will prompt saying the file is not a special device.  Type 'y' to Proceed anyway. 
</div>

This will create 3 directories for a KUBaM setup of 3 nodes.  We now need to create the Kickstart files and copy them into the ```$WORKDIR/kube0$i/``` directories, then unmount the images. 

## 4.1 Kickstart Images

The example in [Section 2.2.1.1 of this Post](http://localhost:4000/os/2017/04/20/centos-redhat-baremetal) will work for our purposes.  We will update this section with more information. 

* Be sure to put a unique IP address for each node
* Substitute your correct encrypted password
* Substitute in your public SSH key as shown in the example. 
* Substitute the mount directory of the tree you created in step 3. This may be something like ```url --url="http://example.com/kubam/rh7.3"``` as we have done in the above example. 

## 4.2 Unmount Kickstart images
Once images are ready, you can unmount them. 
```
for i in $(seq -w 3)
do
	umount $WORKDIR/kube0$i/
done
```
Your files are now ready to go. 

# 5 Take Stock
Check that we now have all the right files:

* http://example.com/kubam/rh7.3 - Installation Media Tree
* http://example.com/kubam/rh7.3-boot.iso - Boot ISO image
* http://example.com/kubam/kube0{1-3}.img - Kickstart Image files

Make sure you can access all of those with your webserver. We will use these for the next step.  

[Go to the Next Stage](http://localhost:4000/kubam/)

