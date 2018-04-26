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

## Monitor

### ```/api/v2/status```

* ```GET``` Get the current overall status of the given server based on the passed parameters.
    * Parameters:
        - type: blade or rack
        - chassis_id: number of the chassis in case of the blade server type
        - slot: number of the blade slot in the chassis in case of the blade server type
        - rack_id: number of the rack server in case of a rack mount server type
        - example: ```/api/v2/status?type=blade&chassis_id=1&slot=4```
    * Returns: ```{
    "completion_time": "2018-04-09T10:42:11.670",
    "current_fsm": "Turnup",
    "fsm_status": "success",
    "progress": "100",
    "sacl": null
}```

### ```api/v2/fsm```

* ```GET``` Get the current detailed status of all FSM stages given server based on the passed parameters.
    * Parameters:
        - type: blade or rack
        - chassis_id: number of the chassis in case of the blade server type
        - slot: number of the blade slot in the chassis in case of the blade server type
        - rack_id: number of the rack server in case of a rack mount server type
        - example: ```/api/v2/status?type=rack&rack_id=2```
    * Returns: 
```
{
    "stages": [
        {
            "descr": "Check if power can be allocated to server 1(FSM-STAGE:sam:dme:ComputePhysicalTurnup:CheckPowerAvailability)",
            "last_update_time": "2018-04-09T10:42:11.093",
            "name": "TurnupCheckPowerAvailability",
            "order": "1",
            "retry": "0",
            "stage_status": "skip"
        },
        {
            "descr": "Waiting for power allocation to server 1(FSM-STAGE:sam:dme:ComputePhysicalTurnup:PowerDeployWait)",
            "last_update_time": "2018-04-09T10:42:11.093",
            "name": "TurnupPowerDeployWait",
            "order": "2",
            "retry": "0",
            "stage_status": "skip"
        },
        {
            "descr": "Power-on server sys/rack-unit-1(FSM-STAGE:sam:dme:ComputePhysicalTurnup:Execute)",
            "last_update_time": "2018-04-09T10:42:11.670",
            "name": "TurnupExecute",
            "order": "3",
            "retry": "1",
            "stage_status": "success"
        }
    ]
}
```

## Servers

### ```/api/v1/servers```

* ```GET``` Get a list of all the UCS Servers and whether they are selected or not.  Also gets the mapping between the OS and the server. 
	* Parameters: None
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
	* Parameters: None
	* Returns: ```{ "status" : "ok"}```




## ISO Images

### ```/api/v1/catalog```

* ```GET```



### ```/api/v1/isos```

* ```GET```  Gets the current ISO files that exist in the ```/kubam/``` directory.  
	* Example: 
	
	```
	curl http://10.93.234.96:8001/api/v1/isos
{
  "isos": [
    "CentOS-7-x86_64-Minimal-1708.iso"
  ]
}

	```




### ```/api/v1/isos/extract```


* ```POST```

### ```/api/v1/isos/boot```

* ```POST```

### ```/api/v1/isos/map```

We Map the file of the operating system to the name of what operating system it is.  We are not smart enough to figure it out in code at this time.  Actually, we are just a little lazy. 

* ```GET``` Gets the current Mapping of OS name to OS iso files.  These are OSes that can be deployed. 
	* Parameters:  None
	* Example:
	```
	curl http://10.93.234.96:8001/api/v1/isos/map
{
  "iso_map": [
    {
      "file": "/kubam/CentOS-7-x86_64-Minimal-1708.iso",
      "os": "centos7.4"
    }
  ]
}
	```


* ```POST``` Maps all ISOS to files.  You should include all previously mapped ISO maps in this request if you want to add one.  KUBAM expects all ISO files to be in the ```/kubam/``` directory of the container.  (this directory is mounted when KUBAM starts from something like ```/root/kubam```.  
   * Parameters: Should be a map of all the isos in the file to the name of the operating systems. 
   	```
   	{
  		"iso_map": [
    		{
      			"file": "/kubam/CentOS-7-x86_64-Minimal-1708.iso",
      			"os": "centos7.4"
    		},
    		{...
    		},
  		]
	}
   	```
	* Example: 
	```
	curl -X POST http://10.93.234.96:8001/api/v1/isos/ma -d '{"iso_map" : [{"os" : "centos7.4", "file" : "/kubam/CentOS-7-x86_64-Minimal-1708.iso"}]}' -H "Content-Type: application/json"
{
  "iso_map": [
    {
      "file": "/kubam/CentOS-7-x86_64-Minimal-1708.iso",
      "os": "centos7.4"
    }
  ]
}
```


## Deploy

### ```/api/v1/deploy```

After all parameters are filled in and boot images have been created the deploy API is used to create the UCS resources.  It logs into UCS Manager and creates the policies, pools, and profiles.  If they have already been created this command does not change them. 

* ```POST```
	* Parameters: None
	* Return: 
	
* ```DELETE```: Delete the UCS resources.  This is a very disruptive command and will completely tear down any UCS servers that are in use. 
	* Parameters: None
	* Return: 





# API v2 
For the next iteration of KUBAM APIs will be refactored to create a better experience. 

## Server Groups

KUBAM stores values for UCS logins inside the ```kubam.yaml``` This API just offers a way to make this happen.  

### ```/api/v2/servers```

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
   ```curl $KUBAM_API/api/v2/servers```
	
	
* ```POST``` - Create a new UCS Domain
	* Params: 
	```
	{"name", "ucs01", "type" : "ucsm", "credentials" : {"user": "admin", "password" : "secret-password", "server" : "172.28.225.163" }}
	```
	
	* Example: ```curl -X POST -H "Content-Type: application/json" -d '{"credentials" : {"user": "admin", "password" : "nbv12345", "ip" : "172.28.225.163" }, "type" : "ucsm", "name" : "devi" }' http://$KUBAM_API/api/v2/servers```
	
* ```PUT``` - Update an existing UCS Domain.  You need to include the UUID of the Domain. Otherwise its the same action as ```POST```. 
* ```DELETE``` - Delete the UCS / CIMC Server Group.  
	* Parameters: ```{"id" : "asdfbasdf..."}```
	* Example: ```curl -X DELETE -H "Content-Type: application/json"  -d '{"id" : "04320631-191c-46f5-a105-a6077661e085"}' $KUBAM_API/api/v2/servers```


## ACI

### ```/api/v2/aci```

* ```GET```: Get all ACI instances.  If there are any there will probably only be one. 
	* Params: ```none```
	
* ```POST```: Create a new ACI instance
	* Params: ```{'name': 'aci01', 'credentials' : {"ip" : "foo", "user" : "admin", "password" : "password"}, "tenant_name" : "blue", "vrf_name" : "lagoon", "bridge_domain" : "3"}```
	* Example: ```curl -X POST -H "Content-Type: application/json" -d '{"name": "aci01", "credentials" : {"ip" : "foo", "user" : "admin", "password" : "password"}, "tenant_name" : "blue", "vrf_name" : "lagoon", "bridge_domain" : "3"}' $KUBAM_API/api/v2/aci```

* ```PUT```: Update an existing ACI instance
	* Params: ```{"id": "someid...", "name": "aci01", "credentials" : {"ip" : "foo", "user" : "admin", "password" : "password"}, "tenant_name" : "blue", "vrf_name" : "lagoon", "bridge_domain" : "3"}```
	* Example: ```curl -X PUT -H "Content-Type: application/json" -d '{"id": "blahblah", "name": "aci0-different", "credentials" : {"ip" : "foo", "user" : "admin", "password" : "password"}, "tenant_name" : "blue", "vrf_name" : "lagoon", "bridge_domain" : "3"}' $KUBAM_API/api/v2/aci```

* ```DELETE```: Delete an existing ACI group
	* Params: ```{"id": "acigroupid"}```
	* Example ```curl -X DELETE -H "Content-Type: application/json" -d '{"id": "blahblah"} $KUBAM_API/api/v2/aci```



## Network Group

### ```/api/v2/networks```

Network parameters are clustered together that can then be added to a server.  

* ```GET```: Get all network settings.
	* Params: ```none```
	* Example:  ```curl -X GET $KUBAM_API/api/v2/networks```
	* Returns:  The current list of network groups
	
	```
	{ "networks" : 
		[
		{"id": "1234-2342-1234-1234-1234",
		"name": "net01", 
		"netmask":"255.255.255.0", 
		"gateway" : "192.168.1.1", 
		"nameserver" : "8.8.8.8", 
		"ntpserver" : "ntp.esl.cisco.com"},
		
		{"id": "1234-2342-1234-1234-1234",
		"name": "net02", 
		"netmask":"255.255.255.0", 
		"gateway" : "192.168.2.1", 
		"nameserver" : "8.8.8.8", 
		"ntpserver" : "ntp.esl.cisco.com"},
		]
	}
	```
* ```POST```: New Network Group
	* Params:  A new Network group
	```
	{ "name": "net01", "netmask" : "255.255.255.0", "nameserver" : "208.67.222.222", "ntpserver" : "ntp.esl.cisco.com", "proxy": "http://proxy.esl.cisco.com:80", "vlan" : "30" }
	```
* ```PUT```: Similar to a POST call but you need to add the ```id``` of the network group you are updating.  This is for modifying an existing network group. 
	* Params: 
	```
	{ "id": "1234-1234-1234-1234" , "name": "newName", "netmask" : "255.255.255.0", "nameserver" : "208.67.222.222", "ntpserver" : "ntp.esl.cisco.com", "proxy": "http://proxy.esl.cisco.com:80", "vlan" : "30" }
	```
* ```DELETE```: Delete existing Network group
	* Params: ```'{"id": "somenetworkid..." }'```
	* Errors:  You should get an error if a network group is already in use by one or most hosts. 

## Hosts

### ```/api/v2/hosts```

* ```GET```: Get all the hosts
    * Params:   ```none```
    * Example:  ```curl -X GET $KUBAM_API/api/v2/hosts```
    * Returns:  Current list of hosts
    
* ```POST```: Update all the hosts.
    *Params:    list of all hosts
    ```
    [
        {'name': 'kube01', 'ip': '172.20.30.1', 'os': 'centos7.4', 'role': 'generic', 'network_group': ''},
        {'name': 'kube02', 'ip': '172.20.30.2', 'os': 'centos7.4', 'role': 'k8s master', 'network_group': '', 'server_group': ''}
    ]
    ```
    
* ```DELETE```: Delete existing Host. 
    * Params:   ```{'name': 'kube01'}```
    * Errors:   An error will occur if there is no hosts to delete.


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


### ```/api/v2/deploy/vmedia```

* ```POST```: Deploys a VMedia policy only that can be used by existing Service Profiles. 

## UCS Actions

### ```/api/v2/ucs/drives```

* ```DELETE``` resets the disk arrays from JBOD to unconfigured good.