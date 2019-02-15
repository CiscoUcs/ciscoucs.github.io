# Configure Service Profiles

KUBAM first requires service profiles with [vmedia policies](https://community.cisco.com/t5/unified-computing-system/using-scriptable-vmedia-with-ucs-manager/ta-p/3638207) be in place.  The idea is once you associate a physical server with a service profile it will immediately get all the bios settings, networking settings, install the operating system (os), and kubernetes in a single step.  To do this you first have to do the following: 

1. Have a service profile template
2. Have a service profile template that uses a vmedia policy. 

You can do this through the GUI, but that is not as cool.  Let's automate this.  

Before, in KUBAM version 1 we did all this for you.  The code is all in there somewhere but we found people had their own ways of doing things and wanted to do this part themselves.  As such, we have made an Ansible method available.  

And now for a rant on Ansible. In the first place, it is much faster to do the configuration of UCS with just straight python as we used to do in KUBAM.  However, Ansible is standard and has a bit more readability (if YAML is your thing).  However, Ansible is pretty slow, and still not my favorite.  Sorry if you a big fan and I just rained on your parade.  But for all its deficiencies it is still better than puppet and chef in terms of being declarative and not requiring dumb agents that just slow things down. End rant. 

## Ansible For UCS

You can start by downloading the [UCS ansible modules](https://github.com/CiscoUcs/ucsm-ansible).  Some of these modules are actually in the official [Ansible distribution](https://docs.ansible.com/ansible/latest/modules/list_of_remote_management_modules.html#ucs).  As an example of some ansible stuff already done, check out [my sample repo](https://github.com/vallard/ucsm-ansible).

In that example in the `site.yaml` file we create a service profile from the source template called `CentOS`.  Then after we create a service profile, we associate it with the server `blade-1`.  You can see the playbook [here](https://github.com/vallard/ucsm-ansible/blob/master/site.yml).

Notice that before we do that, we run a few roles to create the service profile template.  In the [server role](https://github.com/vallard/ucsm-ansible/blob/master/roles/server/tasks/main.yml) we set up:

* BIOS policy with consistent device naming (CDN) this makes it so the interfaces show up as `eno1, eno2, ...`.  I highly recommend it. 
* UUID Pools
* Configure the VMedia Policy for CentOS
* Boot Policy
* Set the boot order (HD first, then VMedia)
* Scrub policy - Once you disassociate the blade we scrub the disk so our install works the next time we run this.  Otherwise, our schema won't work because a blade will boot up and already have an OS on it!
* Maintenance Policy - Reboot right away!  This is dangerous in production!
* Finally, we create the service profile template!

## VMedia For RedHat

A VMedia Policy for RedHat requires two images:

* A CDD image that is common among all nodes
* An HDD image that has the kickstart file that is unique to each node. 

The way we make it unique to each node is to use the service profile name.  So if our service profile is named `node01` then for the HDD image, it will look for `node01.img` file. Below is the ansible playbook to generate this vmedia policy file.  You can then add it to the service profile template.  

You will need to use the KUBAM server as the `remote_ip_address` as that is where both of these files will be created and live.

```
- name: Configure Vmedia Policy
  ucs_managed_objects:
    <<: *login_info
    objects:
    - module: ucsmsdk.mometa.cimcvmedia.CimcvmediaMountConfigPolicy
      class: CimcvmediaMountConfigPolicy
      properties: 
        name: kubam-centos7.5
        retry_on_mount_fail: "yes"
        parent_mo_or_dn: org-root/org-Ansible
        descr: "KUBAM policy"
      children:
      - module: ucsmsdk.mometa.cimcvmedia.CimcvmediaConfigMountEntry
        class: CimcvmediaConfigMountEntry
        properties:
          mapping_name: centos7.5
          device_type: cdd
          mount_protocol: http
          remote_ip_address: 10.93.140.118
          image_name_variable: none
          image_file_name: centos7.5-boot.iso
          image_path: kubam
      - module: ucsmsdk.mometa.cimcvmedia.CimcvmediaConfigMountEntry
        class: CimcvmediaConfigMountEntry
        properties:
          mapping_name: ks
          device_type: hdd
          mount_protocol: http
          remote_ip_address: 10.93.140.118
          image_name_variable: service-profile-name
image_path: kubam
```

## VMedia for VMware

For VMware, the vmedia is just a single ISO image for each node that is unique.  This has to do with the installation properties.  For VMware, we can't mount the kickstart file from a seperate disk like we can with RedHat. 

```
- name: Configure ESXi Policy
  ucs_managed_objects:
    <<: *login_info
    objects:
    - module: ucsmsdk.mometa.cimcvmedia.CimcvmediaMountConfigPolicy
      class: CimcvmediaMountConfigPolicy
      properties:
        name: kubam-esxi
        retry_on_mount_fail: "yes"
        parent_mo_or_dn: org-root/org-Ansible
        descr: "KUBAM ESXi policy"
      children:
      - module: ucsmsdk.mometa.cimcvmedia.CimcvmediaConfigMountEntry
        class: CimcvmediaConfigMountEntry
        properties:
          mapping_name: esxi
          device_type: cdd
          mount_protocol: http
          remote_ip_address: 10.93.140.118
          image_name_variable: service-profile-name
          image_path: kubam
```
 
## VMedia For Ubuntu

For Ubuntu, we are similar to ESXi but the difference is our media we create is much smaller!  Only 50MB compared to the giant ones that VMware and RH create.  This means faster installations, yay!

Basically, you need to map the service profile template name to the ansible playbook. 

```
- name: Configure Ubuntu Policy
  ucs_managed_objects:
    <<: *login_info
    objects:
    - module: ucsmsdk.mometa.cimcvmedia.CimcvmediaMountConfigPolicy
      class: CimcvmediaMountConfigPolicy
      properties:
        name: kubam-ubuntu
        retry_on_mount_fail: "yes"
        parent_mo_or_dn: org-root/org-Ansible
        descr: "KUBAM Ubuntu policy"
      children:
      - module: ucsmsdk.mometa.cimcvmedia.CimcvmediaConfigMountEntry
        class: CimcvmediaConfigMountEntry
        properties:
          mapping_name: ubuntu
          device_type: cdd
          mount_protocol: http
          remote_ip_address: 10.93.140.118
          image_name_variable: service-profile-name
          image_path: kubam
```

## The cart before the horse

Now if you haven't generated all these images yet then this obviously won't work.  Hopefully you have generated all these assets in KUBAM first before doing the node automation part. Then it should come right up!

