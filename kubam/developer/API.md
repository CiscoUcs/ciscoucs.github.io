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
	
* ```DELETE```

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





