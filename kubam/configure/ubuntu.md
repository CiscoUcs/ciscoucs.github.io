# Ubuntu Preseed Files

KUBAM uses preseed to automatically install as explained in the [OS details](https://ciscoucs.github.io/site/OS/UBUNTU.html).  

The default preseed file used by KUBAM is found in the [github tree](https://github.com/CiscoUcs/KUBaM/blob/master/kubam/templates/ubuntu18.04.tmpl).  You may want to customize this to have it install the way you like it.  To do this copy this file into the `~/kubam` directory so that you have the file `~/kubam/ubuntu18.04.tmpl`. 

When building boot images KUBAM will take this file and fill out the template values that were shown in the [Kickstart section](https://ciscoucs.github.io/site/kubam/configure/template.html).  

The preseed file will then be placed in the `~/kubam/ubuntu18.04/preseed/<node>.seed` directory and used as part of the node install. 

The other installation file that is important is the `txt.cfg` file that gets placed in boot CD.  This file is also a template and is in the KUBAM docker file.  It is also in the [github source tree](https://github.com/CiscoUcs/KUBaM/blob/master/kubam/templates/txt.cfg.tmpl).  Notice that by default it uses interface eno1.  Since KUBAM recommends setting the BIOS of the servers to Consistent Device Naming (CDN) this is how the first interface should show up. If you need to change this KUBAM could probably add a variable to put this in the template.  We just haven't done that quite yet. 

Note that when KUBAM builds it does no verification checks of the `preseed` file nor the `txt.cfg` files. So you are on your own here to debug.  
