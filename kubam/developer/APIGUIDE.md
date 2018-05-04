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

# 2. Add UCS Systems

Now we want to add the UCS systems we'll be using.  We may want to carve 1 system up into different chunks to deploy different hosts.  Or maybe the UCS systems will have different network settings.  Whatever.  To do this we add a "server group".  A server group is a collection of actual hardware resources.  It could even be an IMC.  Let's add a few right now. 

We can run: 

```
curl $KUBAM/api/v2/servers
```

Probably nothing here.  So lets add the credentials to log into one of our servers.  Suppose that we have a UCS with 4 blades that we want to put into our server group.  Let's do it: 

Make a file for the server group ```kube-group1.json```:

```
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
     }
   }
```

Now run the POST command with this: 

```
curl -X POST -H "Content-Type: application/json" \
 -d "@./kube-group1.json \
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
      "type": "ucsm"
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





