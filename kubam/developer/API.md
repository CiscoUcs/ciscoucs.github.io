# KUBAM API

KUBAM is developed API first!  The GUI is just a front end and calls the API when updating parts of it. 

The entire API is a python flask application and commands can be seen in the [code itself.](https://github.com/CiscoUcs/KUBaM/blob/master/kubam/app/app.py)

## Status
Simple API to check it the service is still alive.

### ```/```

* ```GET``` returns ```{ "status" : "ok"}``` if the service is up. 

## Session Credentials

KUBAM stores values for UCS logins inside the ```kubam.yaml``` This API just offers a way to make this happen.  

### ```/api/v1/session```

* ```GET```: Get the current credentials
	* Parameters: None
	* Returns: The current credentials without the password.  ``` {
  "credentials": {
    "ip": "172.28.225.163",
    "password": "REDACTED",
    "user": "admin"
  }
}```
	* Error: 
	
* ```POST``` - Add your UCS Credentials into KUBAM
	* Parameters Example: ```{"credentials" : {"user": "admin", "password" : "nbv12345", "server" : "172.28.225.163" }}```
	* Returns: ```{ "login" : "success" }```
	* Error: 
	* Example: ```curl -X POST -H "Content-Type: application/json"  -d '{"credentials" : {"user": "admin", "password" : "nbv12345", "server" : "172.28.225.163" }}' http://172.28.225.135/api/v1/session```
	
* ```DELETE``` - Removes the credentials from the database

## Settings

### ```/api/v1/settings```

* ```POST```

### ```/api/v1/ip```

* ```GET```
* ```POST```

### ```/api/v1/org```

* ```GET```
* ```POST```

### ```/api/v1/proxy```

* ```GET```
* ```POST```

### ```/api/v1/keys```

* ```GET```
* ```POST```

## Networks

### ```/api/v1/networks```

* ```GET``` Get the current network settings of KUBAM including all the UCS VLANs and the current routers, netmask, gateway, etc. 
	* Parameters: None
	* Returns: ```{
  "network": {
    "gateway": "172.28.224.1",
    "nameserver": "171.70.168.183",
    "netmask": "255.255.254.0",
    "ntpserver": "72.163.32.44"
  },
  "vlans": [
    {
      "id": "3095",
      "name": "default",
      "selected": true
    },{ "id": "1", "name": "one", "selected" : false}]}```
* ```POST``` Update the KUBAM networks to get all the 


### ```/api/v1/networks/vlan```

* ```POST```


## Servers

### ```/api/v1/servers```

* ```GET``` Get a list of all the UCS Servers and whether they are selected or not.  Also gets the mapping between the OS and the server. 
	* Parameters: none
	* Returns: 

```
{
  "hosts": [
    {
      "ip": "172.28.225.130",
      "name": "kube01",
      "os": "centos7.4",
      "role": "k8s master"
    },
    {
      "ip": "172.28.225.130",
      "name": "kube01",
      "os": "centos7.4",
      "role": "k8s master"
    }],"servers": [
    {
      "association": "associated",
      "chassis_id": "1",
      "label": "kubam - master",
      "model": "UCSB-B200-M3",
      "service_profile": "org-root/org-devi/ls-devi1",
      "slot": "8",
      "type": "blade"
    },{
      "association": "associated",
      "label": "HX21-Devi - Rk-10",
      "model": "HX240C-M4SX",
      "rack_id": "1",
      "service_profile": "org-root/org-hx-cluster/ls-rack-unit-1",
      "type": "rack"
    }]}   
```

* ```POST```

### ```/api/v1/servers/images```

* ```POST``` Builds the server images.  This is the API to use after all parameters have been filled in.  It will then build ```*.iso``` and ```*.img``` files in the ```~/kubam``` directory. 
	* Parameters: none
	* Returns: ```{ "status" : "ok"}```




## ISO Images

### ```/api/v1/catalog```

* ```GET```



### ```/api/v1/isos```

* ```GET```



### ```/api/v1/isos/extract```


* ```POST```

### ```/api/v1/isos/boot```

* ```POST```

### ```/api/v1/isos/map```

* ```GET```
* ```POST```

## Deploy

### ```/api/v1/deploy```

After all parameters are filled in and boot images have been created the deploy API is used to create the UCS resources.  It logs into UCS Manager and creates the policies, pools, and profiles.  If they have already been created this command does not change them. 

* ```POST```
	* Parameters: none
	* Return: 
	
* ```DELETE```: Delete the UCS resources.  This is a very disruptive command and will completely tear down any UCS servers that are in use. 
	* Parameters: none
	* Return: 





# API v2 
For the next iteration of KUBAM APIs will be refactored to create a better experience. 

## Server Groups

KUBAM stores values for UCS logins inside the ```kubam.yaml``` This API just offers a way to make this happen.  

### ```/api/v2/server-groups```

* ```GET```: Get the current server groups
	* Parameters: None
	* Returns: The current server groups without the password.  It doesn't return all information, just the essential user information. 
	
	```
	{
  		"server-groups": [
    		{"uid": 1, "name" : "ucs01", "type": "ucsm", "credentials" : {"ip" : "192.168.40.1", "user" : "admin", "password" : "encrypted"},
    		{"name" : "ucs02", "type": "ucsm", "credentials" : {"ip" : "192.168.40.20", "user" : "admin", "password" : "encrypted"}
  		]
	}
```
	* Example:
   ```curl $KUBAM_API/api/v2/server-groups```
	
	
* ```POST``` - Create a new UCS Domain
	* Parameters Example: 
	
	```
	{"name", "ucs01", "type" : "ucsm", "credentials" : {"user": "admin", "password" : "secret-password", "server" : "172.28.225.163" }}
	```
	* Returns: ```{ "login" : "success" }```
	* Error: 
	* Example: ```curl -X POST -H "Content-Type: application/json" -d '{"credentials" : {"user": "admin", "password" : "nbv12345", "ip" : "172.28.225.163" }, "type" : "ucsm", "name" : "devi" }' http://$KUBAM_API/api/v2/server-groups```
	
* ```PUT``` - Update an existing UCS Domain.  You need to include the UUID of the Domain. Otherwise its the same action as ```POST```. 
* ```DELETE``` - Delete the UCS / CIMC Server Group.  
	* Parameters: ```{"id" : "asdfbasdf..."}```
	* Example: ```curl -X DELETE -H "Content-Type: application/json"  d '{"id" : "04320631-191c-46f5-a105-a6077661e085"}' $KUBAM_API/api/v2/server-groups```

	

### ```/api/v2/server-groups/{uid}```

* ```GET``` : Get the entire information of one of the server groups
* ```DELETE```: Delete the server group
* ```POST```: Update the server group



## ACI

### ```/api/v2/aci/```

* ```GET```: Get all ACI instances.  If there are any there will probably only be one. 


### ```/api/v2/aci/{uuid}```

* ```GET```: Get the full information of the ACI platform.
* ```POST```: Update the ACI information of a particular ACI group.


## Network Group

### ```/api/v2/networks```

* ```GET```: Get all network settings

### ```/api/v2/networks/{uuid}```

* ```GET```: Get info from perticular network.
* ```POST```: Update the network settings of a particular network group.

## Hosts

### ```/api/v2/hosts```

* ```GET```: Get all the hosts
* ```POST```: Update all the hosts. 


## ISO

### ```/api/v1/catalog```

* ```GET```



### ```/api/v1/isos```

* ```GET```


### ```/api/v1/isos/boot```

* ```POST```

### ```/api/v1/isos/map```

* ```GET```
* ```POST```



## SSH Keys
 
### ```/api/v1/keys```

* ```GET```
* ```POST```

## Deploy 

### ```/api/v2/deploy/images```

Deploy the boot media. 

* ```POST```

Unique or all of them.  Allow multiple servers to be created.  If nothing is passed in, all servers will have boot images created for them. 


### ```/api/v2/deploy/ucs```

Deploy the UCS 

* ```POST```

Unique or all of them.

### ```/api/v2/deploy```

* ```POST``` Does it all for you!  Do the Boot images and deploy UCS. 

## UCS Actions

### ```/api/v2/ucs/drives```

* ```DELETE``` resets the disk arrays from JBOD to unconfigured good.