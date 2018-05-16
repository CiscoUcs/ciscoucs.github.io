# KUBAM YAML file

KUBAM stores everything in YAML file.  The file is created in ```~/kubam/kubam.yaml```.  We show the parts of the YAML file as well as a description of the fields, then at the end show a full example. 
 

### kubam IP

We need the IP address of where the images are hosted.  This is usually the same IP address of the KUBAM server but could be another server where these images are stored. (Although this hasn't been tested)

```
kubam_ip: <kubam_ip>
``` 

### hosts

```
hosts:
- name: <required, unique: hostname / service profile name>
  ip: <required: ipaddress>
  os: <required: operating system>
  role: required: {k8s master, '', k8s node}
  network_group: <required: net group>
  server_group: <optional: server group>
  service_profile_template: <UCS profile template name>
```

Stores the list of hosts.

Name should be unique. Name, ip address, os, role and network_group are required field.
OS specifies what roles host can have.

* ```service_profile_template```: If you want kubam to create a new service profile from this template it will do so instead of creating a whole bunch of new resources. 

### iso map

```
iso_map:
- file: <file directory|url>
  type: {iso_raw, iso_dir, iso_boot}
  os: <os name>
```

The ISO map maps the iso file name to the operating system that KUBAM expects it to be.  When images are created, KUBAM extracts the file to a ```/kubam/tmp/``` directory then moves it to the ```/kubam/<os>``` directory after making sure everything checks out.  

Notice that the container mounts the ```~/kubam``` directory to the ```/kubam``` directory.  That is why you should reference your iso image file in the ```/kubam``` directory.  

The new system here allows for iso's to be hosted elsewhere.  The onlything KUBAM should host is the kickstart files that are automatically generated and created and live on the KUBAM server. 

* ```iso_raw``` - This is the current v1 option where its just a raw option.
* ```iso_dir``` - Exploded directory used for installation so as to not host on the kubam server
* ```iso_boot``` - If you take the kubam generated iso image and want it hosted elsewhere. 



### Network Group

```
network_groups:
- id: <guid>
  name: <required: group name>
  gateway: <required: ip>
  nameserver: <required: ip>
  netmask: <required: netmask: e.g: 255.255.255.0>
  ntpserver: <required: ip>
  vlan: <optional: for VMware sometimes we need a vlan on a trunk port> 
  proxy: <ip, url, etc E.g: http://173.36.224.109:80>
  aci_group: <aci, ''>
- ...
```

Network groups allow different hosts to use different networking parameters to keep them unique.  

On the GUI advanced settings should be shown for: 

* vlan
* proxy
* aci_group

Some notes: 
* VLANs are used for VMware nodes installed on trunk ports with no default vlan.
Each network should specify whether an ACI network is used or 
* Proxy is only set if you are behind a firewall that requires an http proxy to get out to the public network.
* ACI Group is a mapping of the Netmask/Gateway/Settings to an ACI group. 

### ACI Group

```
aci:
- id: <guid>
  name: ACI group name
  credentials:
    ip: <ip>
    password: <secret-password>
    user: <admin>
  tenant_name: <tenant name> 
  tenant_descr: <tenant description>
  vrf_name: <vrf name>
  vrf_description: <vrf descr>
  bridge_domain: <name of bridge domain> 
- ...

```

The ACI group is for inputting settings to ACI.  If a node uses kubernetes and is mapped to an ACI group through the network settings the kubernetes will automatically use the ACI plugins instead of Contiv for kubernetes networking. 
 

### Public Keys
  
```
- <key1>
- <key2>
- ...
```
KUBAM wants you to log in using keypairs and no passwords. An example key would be: 

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCc/7HrOIZB2wk8FvmZXzLMS1ZJ8TvS9OWBf5xosp59NRvcAbwbclLRD2f9z5KvOF1n5a4mK03OetymTQQX08rBpZJZ5ZWztdjiFjIce6rm7V87CRjeuwa97XyhacKx98QcijOJWBbLf1TE/cRd8KVopfG/RPZeMMx1n3J071QRiVhbHEzVw3xuY4KruIb/2kLGHEyYqtx//y8c3k6UaMF180nOIaq6WBZVHnpYXZZ+EkolpJ+10objpueuWPcJe4OU7AIRP1JGsaDHrmXNoy9ygeWceSqOIqRLOdPneHtC6xU78t3ttpnRdC9OgtawIVqaq0wpvd7G0sQ7Jv2DO2hZ
```

### Server Groups

```
server_groups:
- id: <guid>
  name: <server group name>
  type: {imc, ucsm}
  credentials:
    ip: <ip address or hostname>
    password: <password>
    user: <admin>
  org: <org name> | ucsm-only
  vlan: <vlan name> | ucsm-only
  disk_config: {raid 1, ignore, default} | ucsm-only
  server_pool: | ucsm-only
    blades:
    - <chassis-number>/<blade slot>
    - ...
    rack_servers:
    - '<server number>'
```

Server groups are mappings from UCSM login domains so we can support IMC and UCSM to map to. 


