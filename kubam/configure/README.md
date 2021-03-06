# Use KUBAM 

Now that you are installed its time to slap that UCS up into production!

The process works as follows: 

1. You install KUBAM (you did this already right?)  
3. Put in UCS Credentials to KUBAM
4. Configure networking in KUBAM
5. Enter in all the servers you want to deploy into KUBAM
6. Upload ISO images into KUBAM
7. Map ISO images into KUBAM
8. Create the Boot images
9. Create VMedia Policies in UCS, either by hand or some other clever way like Ansible. (We document this approach as well)

For steps 2 - 7 you can either use the KUBAM API or the GUI.  We'll show you how to do that in the upcoming documents.  KUBAM is meant to fit into your automated workflows.  The GUI is just for convenience and still provides a pretty good automated experience. 


Different OSes have different operating system installation methods.  We use the native installer as best we can for each OS.  You can see the methods in the [OS](https://ciscoucs.github.io/site/OS/) section above.  

Kubernetes is only installable on RedHat, CentOS, and Ubuntu.  We use [kubeadm](https://kubernetes.io/docs/setup/independent/install-kubeadm/).  

Support is available [via Twitter](https://twitter.com/vallard). 

The following sections go into details on how to get KUBAM going! 
