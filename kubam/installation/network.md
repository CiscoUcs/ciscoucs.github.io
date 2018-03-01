# Networking Requirements

To make KUBAM work right we have the following requirements:

1. The KUBAM VM/Server must be able to communicate with the UCSM Management IP address.  This is usually a Virtual IP address and is connected to a Gigabit Etherenet interface that comes out of the Fabric Interconnect.  You need this so KUBAM can configure UCS.
2. The UCSM Managemer and CIMCs must be able to communicate with the KUBAM server.  Since the CIMC IP addresses of the nodes should have an IP address on the same subnet as the UCS Manager VIP then you should get this for free.  You need this so the CIMCs can remotely mount the KUBAM installation media. 
3. There should exist a VLAN inside of UCSM that allows the 10Gb+ Etherenet interfaces of the UCS Blades or Rack mount servers through routing or through the same subnet to reach the KUBAM server.  You need this so during the main part of the installation the media is slurped up through the servers actual interface.  
4. With your web browser you should be able to reach the KUBAM web server on port (```5000```) and port (```80```).  You must be able to reach both of those ports.  One is the API server (```80```), the other is the sexy GUI interface (```5000```).

## NATed Interface	Hack

Let's suppose that you have a special instance of KUBAM running behind some sort of fancy NAT setup.  In this example, let's suppose the NAT is ```172.24.90.72``` and port ```8022``` is what we need to ```ssh``` to the KUBAM server.  

In order to see the web interface, you can use SSH port forwarding to do this.  BUT!  You have to forward both the KUBAM web interface and the API since the web interface always thinks the API service is local to it.  

To do this we use [local SSH port forwarding](http://blog.trackets.com/2014/05/17/ssh-tunnel-local-and-remote-port-forwarding-explained-with-examples.html).

In this case we would run two SSH sessions by issuing the following commands: 

```
ssh -L 9000:127.0.0.1:5000 root@172.24.90.72 -p 8022
sudo ssh -L 80:127.0.0.1:80 root@172.24.90.72 -p 8022
```  

Then we can open up the KUBAM web interface on our browser at ```localhost:9000```.  Let's explain the commands:

The first command makes it so our local port ```9000``` is directed to port ```5000``` on the ```172.24.90.72``` server.  We are using port ```8022``` for SSH.  Normally if you are using normal SSH then you could omit this flag and it would just go through port ```22```.  This makes it so we can open our web browser up and point to the KUBAM front end. 

The second command is like the first but it makes it so the API service is exposed on port ```80``` of our local machine.  We have to use ```sudo``` because ```80``` is a privileged port. If you are running something already on port ```80``` then this will not work.  You'll have to shut down your local web service to do this.  
