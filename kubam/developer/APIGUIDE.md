# KUBAM API Guide

Let's suppose you don't want to use the GUI at all but you want to do everything through the KUBAM API.  Here is how you get started.

## Prereqs

KUBAM should be installed and you should have the ISO images of the OSes you want to install in the ```kubam``` directory. 

In the examples the KUBAM server will be ```$KUBAM``` so you may want to set this variable now on the shell:

```
export KUBAM=10.93.234.96:8001
```

## 1. Get the ISOs Mapped

The ISO map tells KUBAM which ISO maps to which OS. Let's first see which ISOs are already in place: 

```
curl $KUBAM/api/v1/isos
```

This might output: 

```
{
  "isos": [
    "en_windows_server_2012_r2_with_update_x64_dvd_4065220.iso",
    "Vmware-ESXi-6.5.0-4564106-Custom-Cisco-6.5.0.2.iso",
    "CentOS-7-x86_64-Minimal-1708.iso",
    "en_windows_server_2016_x64_dvd_9327751.iso"
  ]
}
```

Great, let's see which ISOs are already mapped, if any: 

```
curl $KUBAM/api/v1/isos/map
```

This gives us: 

```json
{
  "iso_map": [
    {
      "file": "/kubam/Vmware-ESXi-6.5.0-4564106-Custom-Cisco-6.5.0.2.iso",
      "os": "esxi6.5"
    }
  ]
}
```
It probably wouldn't give you anything if you didn't have anything.  Let's map one of the ISOs: 

```
curl -X POST -d '{"iso_map" : [{"file": "/kuam/CentOS-7-x86_64-Minimal-1708.iso", "os": "centos7.4"}, {"file": "/kubam/Vmware-ESXi-6.5.0-4564106-Custom-Cisco-6.5.0.2.iso", "os": "esxi6.5"} ]}' -H "Content-Type: application/json" $KUBAM/api/v1/isos/map
```

Notice a few things here:  

* you have to add ```/kubam``` to the file name
* make sure you add ```-H "Content-Type: application/json"``` or it won't send. 

### Seeing what is supported

You may be wondering what OSes KUBAM can support. You can find that with 

```
curl $KUBAM/api/v1/catalog
```

From the output here you can see which "os" you can put down in the commands above. 

Great, now we have our ISO images up. 

## 2. Add UCS Systems

Now we want to add the UCS systems we'll be using.  We may want to carve 1 system up into different chunks to deploy different hosts.  Or maybe the UCS systems will have different network settings.  Whatever.  To do this we add a "server group".  A server group is a collection of actual hardware resources.  It could even be an IMC.  Let's add a few right now. 

We can run: 

```
curl $KUBAM/api/v2/servers
```

Probably nothing here.  So lets add the credentials to log into one of our servers.  Suppose that we have a UCS with 4 blades that we want to put into our server group.  Let's do it: 

Make a file for the server group ```kube-group1.json```:

```json
{
     "name": "kube-group1",
     "credentials": {
       "user": "admin",
       "password": "CiscoPassword",
       "ip" : "172.28.225.163"
     },
     "type": "ucsm",
     "server_pool": {
       "blades": [
     	  "1/1", "1/2", "1/3", "1/4"
       ]
     },
     "vlan" : "default"
   }
```

Now run the POST command with this: 

```
curl -X POST -H "Content-Type: application/json" \
 -d "@./kube-group1.json" \
$KUBAM/api/v2/servers
```

We could add another server group as well.  It can even be the same UCS with those credentials.  Now we can check to make sure we have entered the Server Group information:

```
curl $KUBAM/api/v2/servers
```

You'll see that this group is given an ID and the password is encrypted. 

```
{
  "servers": [
    {
      "credentials": {
        "ip": "172.28.225.163",
        "password": "gAAAAABa7LpjGwKgGjspR4eqQyNm4ockVDVQsilOzYW0Zvha5A9AErexg46ejWE_UFMql68eDudiykxfOdf6-cdfXbOiI2luig==",
        "user": "admin"
      },
      "id": "6e10b961-3f9c-4ce3-926c-a8e1471c24f4",
      "name": "kubernetes",
      "server_pool": {
        "blades": [
          "1/1",
          "1/2",
          "1/3",
          "1/4"
        ]
      },
      "type": "ucsm",
      "vlan": "default"
    }
  ]
}
```

Let's add a C Series server as well.  Make a file called ```c-series1.json``` with the contents like:

```json
{
  "name": "c240-01",
  "credentials": {
    "user": "admin",
    "password": "CiscoPassword",
    "ip" : "10.93.234.140"
   },
   "type": "imc"
}
```
Now we can add it with the same command we ran previously: 

```
curl -X POST -H "Content-Type: application/json" \
 -d "@./c-series1.json \
$KUBAM/api/v2/servers
```

## 3. Settings 

### 3.1 SSH Keys

We want to keep access to our servers secure.  Therefore we disable passwords and use SSH keys. We add a list of SSH keys with KUBAM that have access to the servers. This can be done by createing a file: ```ssh-keys.json``` and having the contents look like:  

```json
{"keys" : [
	"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCc/7HrOIZB2wk8FvmZXzLMS1ZJ8TvS9OWBf5xosp59NRvcAbwbclLRD2f9z5KvOF1n5a4mK03OetymTQQX08rBpZJZ5ZWztdjiFjIce6rm7V87CRjeuwa97XyhacKx98QcijOJWBbLf1TE/cRd8KVopfG/RPZeMMx1n3J071QRiVhbHEzVw3xuY4KruIb/2kLGHEyYqtx//y8c3k6UaMF180nOIaq6WBZVHnpYXZZ+EkolpJ+10objpueuWPcJe4OU7AIRP1JGsaDHrmXNoy9ygeWceSqOIqRLOdPneHtC6xU78t3ttpnRdC9OgtawIVqaq0wpvd7G0sQ7Jv2DO2hZ", 
	"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCd2XeDE/Ev5TJxBRAmrsTglAQQG8v5JZ8VoOUdSBUCONcJilcERdpOtGOgJR4t1xr2r0G3oDZrRGEaS5/Kjo91/LIxOR01aUgNb6zFkrSdlu8ktBmLsEvocG68di3GGG9JqoICL8CoPLkRDWGcBO3GKhOEd0TEK1hwUeGOX0NBMBERQtGXPiHq4tXvoUSyzsUSdAKypfRlKJgCETG9muGmHAtF1Z5pJXq8BqiiZ/GKm8Z6R60Z8hEQnNzIySyUHp1J6wvgnsZAVrUSMTclQ8NBrnagLVPToU5SI2zXGdiVIPh9enda+warwF5TuW80EABCbEIUtbqwde2nbqIlQOP5"
]}
```

These keys can then be added to the API with: 

```
curl -X POST -d "@./ssh-keys" -H "Content-Type: application/json" $KUBAM/api/v1/keys
```

To see that the keys are there you can run: 

```
curl $KUBAM/api/v1/keys
```
Then the keys will all be returned. 

### 3.2 KUBAM IP

The servers need to know where they should get their install images from.  Typically this is the same IP address of the KUBAM server, but you might be able to host the files elsewhere and change this IP.  We will use the KUBAM IP address: 

```
curl -X POST -d '{ "kubam_ip": "10.93.234.96" }' -H "Content-Type: applicaton/json" $KUBAM/api/v1/ip
```

## 4. Add Networking Details

Each host when installed needs a network configured.  Many hosts will share the same networking constructs such as gateway, DNS, subnet, etc.  To make mapping common network constructs to hosts and to avoid repitition KUBAM uses the idea of a "Network Group".  The network group just contains common networking characteristics that a host would use.  A network group can be mapped to multiple hosts but a host can only map to one network group. 

To add a network group create a file with the network group characteristics called ```netgrp1.json```.  The contents will be: 

```
{
  "name": "net01",
  "netmask" : "255.255.254.0",
  "nameserver" : "171.70.168.183",
  "gateway": "172.28.224.1",
  "ntpserver" : "72.163.32.44",
  "proxy": "http://proxy.esl.cisco.com:80",
  "vlan" : "30"
}
```
A few comments about the values:

* The name should be unique but can be changed.
* The proxy and vlan are optional.  The rest are not.
* The VLAN is for ESXi templates if the management nic doesn't have a native VLAN and if one needs to be specified.  Usually you will leave this out. 
* Proxy is for hosts that are behind firewalls like most of the environments we work on internally in Cisco. This is a way the host can get to the outside network if post install scripts (like kubernetes) need to access containers.  Leave this out if not needed.
* The netmask, gateway, nameserver, and ntpserver will be installed in the host. 

To add this we run: 

```
curl -X POST -H "Content-Type: application/json" -d "@./netgrp1.json" $KUBAM/api/v2/networks
```
We get back something like: 

```
{
  "status": "Network net01 created!"
}
```

Performing a ```GET``` call and we can get back all of the details: 

```
curl $KUBAM/api/v2/networks
```
The output will be all the networks

```
{
  "networks": [
    {
      "gateway": "172.28.224.1",
      "id": "60b25585-c1ff-4ff5-947a-9f171bd6ed38",
      "name": "net01",
      "nameserver": "171.70.168.183",
      "netmask": "255.255.254.0",
      "ntpserver": "72.163.32.44",
      "proxy": "http://proxy.esl.cisco.com:80",
      "vlan": "30"
    }
  ]
}
```
Notice however that there is an ```id``` that was created.  If we want to delete this network we use the ```DELETE``` with ```{"id": "60b25585-c1ff-4ff5-947a-9f171bd6ed38"}``` to delete it.  

If we want to rename it then we must do a ```PUT``` operation and include the ```id``` and all the values we wish to update. This is different than some of the KUBAM resources as we can work on them individually.

## 5. Hosts

We now come to the main event where we specify what hosts we will deploy.  We create a ```hosts.json``` file that includes all the hosts we wish to deploy.  This includes the mapping to network groups and server groups.  This is where we need the ```id```s of those groups.  The contents looks as follows:

```
[
    {
      "name": "kubam01",
      "ip": "172.28.225.130",
      "os": "centos7.4",
      "role": "generic",
      "network_group": "net01",
      "server_group": "kube-group1",
      "service_profile_template": "org-root/ls-myprofile"
    },
    {
      "name": "kubam02",
      "ip": "172.28.225.131",
      "os": "esxi6.5",
      "role": "generic",
      "network_group": "net01"
    },
    {
      "name": "kubam03",
      "ip": "172.28.225.132",
      "os": "win2016",
      "role": "generic",
      "network_group": "net01"
    }
]
```

* The ```network_group``` and ```server_group``` will need to match the ```name``` of those groups. 
* ```os``` and ```roles``` will need to be defined from the ```/api/v1/catalog```
* The ```network_group``` __is required__ the ```server_group``` however is not required and can be omitted if you want to add the boot images yourself. 
* Hostnames need to match the service profile name or the vMedia policy will not work. 
* Hosts in the same ```server_group``` must use the same Operating system.  You can't install ```esxi6.5``` and ```centos7.4``` in the same server group.  Only one can be selected. 

Call this to add the hosts: 

```
curl -X POST -d "@./hosts.json" $KUBAM/api/v2/hosts
```



## 6. Installation image creation

With all the parameters we are now set to deploy the boot images.  Creating the boot images usually comprises of the following steps that KUBAM performs for you: 

* Extracts the ISO image for use of the OS installation in the ~/kubam directory. 
* Creates a Boot ISO image if this isn't already created for you.
	* In the case of Windows, this step you must perform manually.  KUBAM checks to make sure the ```WinPE_KUBAM.iso``` image has been uploaded. 
	* In the case of ESXi a unique boot ISO is created for each host.  Yes this sucks, but we haven't put more time into this yet to make it better.  Disk space is cheap, life is short. Open an issue if this bugs you. 
	* In the case of RedHat/CentOS a special boot iso is created if there is not one in place already. 

* Creates individual 1MB hard drive images for each host (except for VMware since this is bundled in the OS ).  It takes a template that comes by default with KUBAM or a template in the ```~/kubam``` directory, such as ```centos7.4.tmpl``` or ```win2016.tmpl``` and fills in values.  


To set up the images we run: 

```
curl -X POST $KUBAM/api/v2/deploy/images
```

With no arguments all server images will be created.  To do just a few we can do: 

```
curl -X POST -d '["kubam01", "kubam02"]' $KUBAM/api/v2/deploy/images
```

Each time this is done the ```<host>.img``` file will always be rewritten.  If the boot image and ISO image already exists it will not be changed.  You would have to delete them if you wanted them to be regenerated. 

## 7. UCS Deployment

If at this point the images are created we can now deploy the UCS resources.  This is done with 

```
curl -X POST $KUBAM/api/v2/servers/<server_group_name>/deploy
```

* If the host has a ```service_profile_template``` created we will create a new service profile based on that template. If there is also a node associated: ```1/3``` then we will bind to that blade.
* If there is no  ```service_profile_template``` or host associated, we will make a service profile template called ```KUBAM_<os>``` and then put the servers in a pool and map the blades. (This is the behavior similar to how version 1 of KUBAM worked) 


```
curl -X POST $KUBAM/api/v2/servers/<server_group_name>/vmedia
```

* Deploy ONLY the vmedia policy of the nodes in this server group. 
 








