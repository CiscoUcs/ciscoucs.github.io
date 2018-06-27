# KUBAM Kubernetes Proposal

KUBAM's kubernetes deployment includes the following: 

* Use a *very* small Alpine Linux distribution for the bare metal installation
* Use the upstream vanilla Kubernetes binaries
* Include contiv-vpp networking
* Include other components required to make a full kubernetes distribution.  


# Notes

We first start out with the 105MB alpine 3.7 image.  This image is looped then copied to another directory.  

There are two files that we can trim down: 

```
modloop-hardened
```
and
 
```
initramfs-hardened
```

To see what's in modloop-hardened: 

```
unsquashfs -l /boot/modloop-hardened
```

To see initramfs: 

```
gzip -dc /boot/initramfs-hardened | cpio -it
```

We need to do the following: 

* Add basic packages: docker, ssh, etc
* Configure networking, commands to startup

To add basic packaging: 

```
http://dl-cdn.alpinelinux.org/alpine/edge/main
http://dl-cdn.alpinelinux.org/alpine/edge/community
```

```
apk update
```

```
apk install docker
rc-update add docker boot
service docker start
```
[More information](https://wiki.alpinelinux.org/wiki/Docker#Installation)




### Making the ISO file

```
cd mounted image dir
```

Now run: 

```
cd alpine-3.7
ls # you should see boot and apks 
mkisofs -o ../alpine-kubam.iso \
	-b boot/syslinux/isolinux.bin \
	-c boot/syslinux/boot.cat \
	-no-emul-boot \
	-V "alpine-standard 3.7.0 x86_64" \
	-boot-load-size 4 -boot-info-table -r -J -v \
	-T .
```

### Changing the modules 
We can add and remove modules to the modules squashfs image. 


```
mkdir modloop
cd modloop
unsquashfs ../boot/modloop-hardened
```
Change things in there.  Then put it back up

```
mksquashfs squashfs-root modloop-hardened
mksquashfs  squashfs-root modloop-hardened -b 1048576 -comp xz -Xdict-size 100% # be sure to remove original
```

Things to get rid of: 

```
firmware/nvidia
firmware/amdgpu
firmware/qlogic
firmware/3com
firmware/rtl_nic
firmware/rtlwifi
firmware/iwlwifi*
firmware/sun
firmware/brcm
firmware/bnx2
firmware/bnx2x
firmware/yamaha
firmware/ql*
modules/4.9.65-1-hardened/kernel/fs/9p
modules/4.9.65-1-hardened/kernel/fs/cifs
modules/4.9.65-1-hardened/kernel/fs/ceph
modules/4.9.65-1-hardened/kernel/fs/reiserfs
modules/4.9.65-1-hardened/kernel/drivers/gpu
modules/4.9.65-1-hardened/kernel/drivers/video
modules/4.9.65-1-hardened/kernel/drivers/xen
modules/4.9.65-1-hardened/kernel/drivers/thunderbolt
modules/4.9.65-1-hardened/kernel/drivers/infiniband
modules/4.9.65-1-hardened/kernel/drivers/firewire
modules/4.9.65-1-hardened/kernel/drivers/net/ethernet/qlogic
modules/4.9.65-1-hardened/kernel/drivers/net/ethernet/mellanox
modules/4.9.65-1-hardened/kernel/drivers/net/ethernet/fujitsu
modules/4.9.65-1-hardened/kernel/drivers/net/ethernet/3com
modules/4.9.65-1-hardened/kernel/drivers/net/ethernet/broadcom
modules/4.9.65-1-hardened/kernel/drivers/net/ethernet/chelsio
modules/4.9.65-1-hardened/kernel/drivers/net/wireless
modules/4.9.65-1-hardened/kernel/drivers/net/wimax