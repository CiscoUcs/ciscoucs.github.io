---
layout: page
title: KUBaM! - Stage 2 UCSM Python SDK
tags: Kubernetes, containers
---

Before continuing, be sure you have completed [stage 1](http://localhost:4000/kubam/).  

# 1. Prereqs

* Python 2.7+ is required
* The build machine could be the same as the web server machine but should be able to access UCSM with a ping.

# 2. Setup

## 2.1 Get Python Setup

RedHat and CentOS should come with python installed by default.  You'll just need to get pip to get the UCS dependencies. 

```
cd /tmp/
curl https://bootstrap.pypa.io/get-pip.py
python get-pip.py
pip install ucsmsdk
```

<div class="alert alert-info">
<b>Proxy Issues?</b> If you are behind a proxy you may need to enter in the proxy information for the git clone to work.  Example:   
<code>
https_proxy=proxy.esl.cisco.com:80 curl https://bootstrap.pypa.io/get-pip.py</code>
You may also need to prepend the other commands with this proxy information. 
</div>


## 2.2 Get the code:

```
mkdir -p ~/Code
cd Code
git clone https://github.com/vallard/KUBaM.git
cd KUBaM/
```

<div class="alert alert-info">
<b>Proxy Issues?</b> If you are behind a proxy you may need to enter in the proxy information for the git clone to work.  Example:   
<code>
https_proxy=proxy.esl.cisco.com:80 git clone https://github.com/vallard/KUBaM.git
</code>
</div>



# 3. Run the Installation Script

```
cd ~/Code/KUBaM/stage2
./kubeucs.py admin cisco.123 172.28.225.102
[1] VLAN default
[2] VLAN hx-inband-mgmt
[3] VLAN hx-vmotion
[4] VLAN hx-data
[5] VLAN Docker-Data
[6] VLAN Docker-storage
[7] VLAN hx-storage-data
[8] VLAN vm-network
--------------------------------------------------------------------------------
Please Select a VLAN for the Kubernetes Server to use: 1
Creating Kubernetes MAC Pools
Creating Kubernetes VNIC Templates
Creating Kubernetes LAN connectivity policy
Creating Kube Boot Policy
Creating Kube Local Disk Policy
Creating Kube UUID Pools
Creating Kubernetes Compute Pool
Adding Virtual Media Policy
What is the URL for the Boot ISO image?
(E.g.: http://192.168.2.2/kubam/centos7.2-boot.iso) : http://172.28.225.80/kubam/rh73-boot.iso
You entered: http://172.28.225.80/kubam/rh73-boot.iso
Is this correct? [y/N]: y
Listing available UCS Servers
[1]: Blade 1/slot-3 type UCSB-B200-M3
[2]: Blade 1/slot-5 type UCSB-B200-M3
[3]: Blade 1/slot-6 type UCSB-B200-M3
[4]: Blade 1/slot-7 type UCSB-B200-M3
[5]: Blade 1/slot-8 type UCSB-B200-M3
Please select servers you want to install Kubernetes on separated by commas
(E.g: 2,4,8) :
```

At the end of this script, the servers should boot back up and be provisioned with the OS you created and be ready to go. 



