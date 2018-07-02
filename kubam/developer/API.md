# KUBAM API

KUBAM is developed API first!  The GUI is just a front end and calls the API when updating parts of it. 

The entire API is a python flask application and commands can be seen in the [code itself.](https://github.com/CiscoUcs/KUBaM/blob/master/kubam/app/app.py)

## Status
Simple API to check it the service is still alive.

### ```/```

* ```GET``` returns ```{ "status" : "ok"}``` if the service is up. 


## Settings

### ```/api/v1/ip```

Set the IP address of the boot server.  Usually this is just the KUBAM server. This is so the nodes where to get install media when they boot up.  KUBAM also uses this to set the vmedia policy to connect to this IP address. 

* ```POST```
	* Example
	
	```
	curl -X POST -d '{ "kubam_ip": "10.93.234.96" }' -H "Content-Type: applicaton/json" $KUBAM/api/v1/ip
	```

### ```/api/v1/keys```

* ```GET``` - Returns a list of the Public SSH Keys that have been entered into KUBAM.  These keys are ones that hosts can use to ssh into the servers installed by KUBAM. 
	* Example:
	
	```
	curl 172.28.225.135/api/v1/keys
{
  "keys": [
    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCc/7HrOIZB2wk8FvmZXzLMS1ZJ8TvS9OWBf5xosp59NRvcAbwbclLRD2f9z5KvOF1n5a4mK03OetymTQQX08rBpZJZ5ZWztdjiFjIce6rm7V87CRjeuwa97XyhacKx98QcijOJWBbLf1TE/cRd8KVopfG/RPZeMMx1n3J071QRiVhbHEzVw3xuY4KruIb/2kLGHEyYqtx//y8c3k6UaMF180nOIaq6WBZVHnpYXZZ+EkolpJ+10objpueuWPcJe4OU7AIRP1JGsaDHrmXNoy9ygeWceSqOIqRLOdPneHtC6xU78t3ttpnRdC9OgtawIVqaq0wpvd7G0sQ7Jv2DO2hZ\n"
  ]
}
	```

* ```POST``` - Add or change public keys.  The keys are a list of Public ssh keys. KUBAM uses these keys to allow nodes to be accessed by these keys when installed.  
	* Params: 
	
	```
	{"keys" : [
	"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCc/7HrOIZB2wk8FvmZXzLMS1ZJ8TvS9OWBf5xosp59NRvcAbwbclLRD2f9z5KvOF1n5a4mK03OetymTQQX08rBpZJZ5ZWztdjiFjIce6rm7V87CRjeuwa97XyhacKx98QcijOJWBbLf1TE/cRd8KVopfG/RPZeMMx1n3J071QRiVhbHEzVw3xuY4KruIb/2kLGHEyYqtx//y8c3k6UaMF180nOIaq6WBZVHnpYXZZ+EkolpJ+10objpueuWPcJe4OU7AIRP1JGsaDHrmXNoy9ygeWceSqOIqRLOdPneHtC6xU78t3ttpnRdC9OgtawIVqaq0wpvd7G0sQ7Jv2DO2hZ", 
	"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCd2XeDE/Ev5TJxBRAmrsTglAQQG8v5JZ8VoOUdSBUCONcJilcERdpOtGOgJR4t1xr2r0G3oDZrRGEaS5/Kjo91/LIxOR01aUgNb6zFkrSdlu8ktBmLsEvocG68di3GGG9JqoICL8CoPLkRDWGcBO3GKhOEd0TEK1hwUeGOX0NBMBERQtGXPiHq4tXvoUSyzsUSdAKypfRlKJgCETG9muGmHAtF1Z5pJXq8BqiiZ/GKm8Z6R60Z8hEQnNzIySyUHp1J6wvgnsZAVrUSMTclQ8NBrnagLVPToU5SI2zXGdiVIPh9enda+warwF5TuW80EABCbEIUtbqwde2nbqIlQOP5"
	]}
	```


## Monitor

### ```/api/v2/servers/<server-group>/status```

* ```GET``` Get the current overall status of the given server based on the passed parameters.
	* Examples:
	
	```
	curl -X GET -d '{"servers": {"blades": ["1/3"], "rack_servers" : ["1"]}}' -H "Content-Type: application/json" $KUBAM_API/api/v2/servers/kube-group1/status
	```
	
	Entering no parameters gets the status of every node
	
	```
	curl $KUBAM_API/api/v2/servers/kube-group1/status
	```
   
    * Returns: 

    ```
  	{
  		"servers": {
    		"blades": {
      			"1009/1/1": {
        			"association": "associated",
        			"chassis_id": "1",
        			"dn": "compute/sys-1009/chassis-1/blade-1",
        			"domain_id": "1009",
        			"label": "",
        			"model": "UCSB-B200-M4",
        			"num_cores": "36",
        			"num_cpus": "2",
        			"oper_power": "off",
        			"ram": "393216",
        			"ram_speed": "1866",
        			"service_profile": "org-root/org-SLCLAB3/ls-SLC-RDO_OS-01",
        			"slot": "1",
        			"type": "blade"
      			},
      		...
      		}
     		"rack_servers": {
       		"1009/1" : {
       			...
       		}
       		...
     		}
     	}
    }
    ```
    (The above output is for UCS Central.  UCS Manager shows similar but omits the domain id (1009) from the blade name.)


### ```/api/v2/fsm```

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
	
	
* ```POST``` - Create a new Server group
	* Params: 
	```
	{"name", "ucs01", "type" : "ucsm", "credentials" : {"user": "admin", "password" : "secret-password", "ip" : "172.28.225.163" }}
	```
	
	* Example: ```curl -X POST -H "Content-Type: application/json" -d '{"credentials" : {"user": "admin", "password" : "nbv12345", "ip" : "172.28.225.163" }, "type" : "ucsm", "name" : "devi" }' http://$KUBAM_API/api/v2/servers```
	
* ```PUT``` - Update an existing UCS Domain.  You need to include the UUID of the Domain. Otherwise its the same action as ```POST```. 
* ```DELETE``` - Delete the UCS / CIMC Server Group.  
	* Parameters: ```{"name" : "asdfbasdf..."}```
	* Example: ```curl -X DELETE -H "Content-Type: application/json"  -d '{"name" : "net1"}' $KUBAM_API/api/v2/servers```

	
### ```/api/v2/servers/<server_group>/power/<power-action>```

These methods change the power cycle of the server
 
* ```PUT``` - change the power cycle of a server.  The methods that are allowed are: 
	* ```on```
	* ```off```
	* ```hardreset```
	* ```softreset```

	* Example: 
	```
	curl -X PUT -d '{"servers" : {"blades" : ["1/3"], "rack_servers" : ["1"]}}' -H "Content-Type: application/json" $KUBAM_API/api/v2/servers/kube-group1/power/on
	```
	* Example Output: 
	
	```json
	{
  		"status": {
   			"blades": [
      			"1/3: off"
    		],
    		"rack_servers": [
      			"1: off"
    		]
  		}
	}	
	```
	* Example (UCS Central):
	
	```
	curl -X PUT -d '{"servers" : {"blades" : ["1009/1/1"] }}' -H "Content-Type: application/json" $KUBAM_API/api/v2/servers/drury-central/power/on
	```
	__(Note: it takes a little bit for the status to change from off to on.)__

### ```/api/v2/servers/<server_group>/powerstat```

* ```GET``` - Returns the power status of a server.
	* Example:
	```
	curl -X GET -d '{"servers": {"blades": ["1/3"], "rack_servers" : ["1"]}}' -H "Content-Type: application/json" $KUBAM_API/api/v2/servers/kube-group1/powerstat
	```
	* Example Output:
	
	```json
	{
  		"status": {
    		"blades": [
      			"1/3: on"
    		],
    		"rack_servers": [
      			"1: on"
    		]
  		}
	}
	
	```
	* Example: You can also get all the servers by not passing in any arguments
	
	```
	curl $KUBAM_API/api/v2/servers/kube-group1/powerstat
	```


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
	* Example ```curl -X DELETE -H "Content-Type: application/json" -d '{"name": "blahblah"} $KUBAM_API/api/v2/aci```



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
	* Params: ```'{"name": "somenetworkname..." }'```
	* Errors:  You should get an error if a network group is already in use by one or most hosts. 

## Hosts

### ```/api/v2/hosts```

* ```GET```: Get all the hosts
    * Params:   ```none```
    * Example:  ```curl -X GET $KUBAM_API/api/v2/hosts```
    * Returns:  Current list of hosts
    
* ```POST```: Update all the hosts.
    * Params:    list of all hosts
    
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


```
[ "host1", "host2", "host3", ...]
```


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