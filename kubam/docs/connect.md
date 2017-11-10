---
layout: page
title: KUBAM! Advanced Connections
tags: Kubernetes, containers
---
{% include JB/setup %}

## NATed Interface	

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