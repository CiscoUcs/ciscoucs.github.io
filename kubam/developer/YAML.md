# KUBAM YAML file


## Version 1 (current)

KUBAM stores everything in YAML file.  The file is created in ```~/kubam/kubam.yaml```.  We show the parts of the YAML file as well as a description of the fields, then at the end show a full example. 

### hosts
```
hosts:
- ip: <ipaddress>
  name: <hostname / service profile name
  os: <operating system>
  role: {k8s master, '', k8s node}

```

Each host is an item in the host list.  It is important to note that the ```name``` will be the hostname and the service profile name.  You should not use a fully qualified domain name (FQDN) for the name.  KUBAM requires that the hostname = service profile name. 

### iso map

```
iso_map:
- file: <file directory>
  os: <os name>
```

The ISO map maps the iso file name to the operating system that KUBAM expects it to be.  When images are created, KUBAM extracts the file to a ```/kubam/tmp/``` directory then moves it to the ```/kubam/<os>``` directory after making sure everything checks out.  

Notice that the container mounts the ```~/kubam``` directory to the ```/kubam``` directory.  That is why you should reference your iso image file in the ```/kubam``` directory.  

### kubam IP
```
kubam_ip: <kubam_ip>
```
This should be the IP address of the KUBAM VM/server. 

### network

```
network:
  gateway: <ip>
  nameserver: <ip>
  netmask: <netmask: e.g: 255.255.255.0>
  ntpserver: <ip>
```
These parameters are applied to all servers in kubam. KUBAM v1 doesn't support installing nodes on different networks... yet. 

### proxy

```
proxy: <ip, url, etc. E.g: http://173.36.224.109:80>
```
Use this only if you are behind a firewall that requires an http proxy to get out to the public network. 

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

### UCS Settings

```
ucsm:
  credentials:
    ip: <ip address or hostname>
    password: <password>
    user: <admin>
  org: <org name>
  ucs_network:
    vlan: <vlan name>
  ucs_server_pool:
    blades:
    - <chassis-number>/<blade slot>
    - ...
    rack_servers:
    - '<server number>'
```

The settings define how to contact a particular UCS as well as what blades and rack mount servers are defined.


### Full Example

```yaml
hosts:
- ip: 172.28.225.130
  name: kube01
  os: centos7.4
  role: k8s master
- ip: 172.28.225.131
  name: kube02
  os: centos7.4
  role: k8s node
- ip: 172.28.225.132
  name: kube03
  os: centos7.4
  role: k8s node
- ip: 172.28.225.133
  name: kubam-test
  os: centos7.4
  role: ''
- ip: 172.28.225.134
  name: kubam-test2
  os: centos7.4
  role: ''
iso_map:
- file: /kubam/CentOS-7-x86_64-Minimal-1708.iso
  os: centos7.4
kubam_ip: 172.28.225.135
network:
  gateway: 172.28.224.1
  nameserver: 171.70.168.183
  netmask: 255.255.254.0
  ntpserver: 72.163.32.44
proxy: http://173.36.224.109:80
public_keys:
- ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCc/7HrOIZB2wk8FvmZXzLMS1ZJ8TvS9OWBf5xosp59NRvcAbwbclLRD2f9z5KvOF1n5a4mK03OetymTQQX08rBpZJZ5ZWztdjiFjIce6rm7V87CRjeuwa97XyhacKx98QcijOJWBbLf1TE/cRd8KVopfG/RPZeMMx1n3J071QRiVhbHEzVw3xuY4KruIb/2kLGHEyYqtx//y8c3k6UaMF180nOIaq6WBZVHnpYXZZ+EkolpJ+10objpueuWPcJe4OU7AIRP1JGsaDHrmXNoy9ygeWceSqOIqRLOdPneHtC6xU78t3ttpnRdC9OgtawIVqaq0wpvd7G0sQ7Jv2DO2hZ
ucsm:
  credentials:
    ip: 172.28.225.163
    password: secret-password
    user: admin
  org: root
  ucs_network:
    vlan: default
  ucs_server_pool:
    blades:
    - 1/1
    - 1/3
    - 1/5
    - 1/7
    rack_servers:
    - '7'
```

Notice in kubam v1 the password is stored in plain text.  This is clearly a bad idea. 

## Version 2 (Proposed)

KUBAM stores everything in YAML file.  The file is created in ```~/kubam/kubam.yaml```.  We show the parts of the YAML file as well as a description of the fields, then at the end show a full example. 


### hosts

```
hosts:
- name: <required, unique: hostname / service profile name>
  ip: <required: ipaddress>
  os: <required: operating system>
  role: required: {k8s master, '', k8s node}
  network_group: <required: net group>
  server_group: <optional: server group>
```

Stores the list of hosts.

Name should be unique. Name, ip address, os, role and network_group are required field.
OS specifies what roles host can have.

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

### kubam IP
```
kubam_ip: <kubam_ip>
```
This should be the IP address of the KUBAM VM/server.


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


