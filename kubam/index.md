---
layout: page
title: KUBaM! - Kubernetes on UCS Bare Metal
tags: Kubernetes, containers
---
{% include JB/setup %}

 

You have UCS and you want Kubernetes running on it as fast as possible. Before you can even say KUBaM we will make that happen.  Here we outline the steps and process of how this all goes down.  Want to see a quick tour?  Watch the video below

<iframe width="560" height="315" src="https://www.youtube.com/embed/_6IBeywMoMA" frameborder="0" allowfullscreen></iframe>

You may also have ways you like doing things with your tools.  Therefore, in each stage we have and will continue to add options of how each stage can be accomplished.  Have a tool?  [Let us know](http://twitter.com/vallard) and we'll prioritize it. 

Installing Kubernetes on UCS Bare Metal is a 4 stage process.   At each stage you may have several options and we will add options as they become available.  
## Stage 1 - Prepare 
You will need a management server that has all the bits required for the kubernetes setup.

* __Recommended:__ [Using Docker](/kubam/stage1/docker)  
* [Manual Preparation](/kubam/stage1/manual)

## Stage 2 - UCS Bare Metal Deployment

In this stage you will need to setup UCS service profiles in a way so they automatically install the operating system. 

* [UCSM Python Scripts](/kubam/stage2/python)

## Stage 3 - Install Kubernetes

Here we automate the installation process of Kubernetes on operating systems that are now provisioned. 

* [Ansible Scripts](/kubam/stage3/ansible)

## Stage 4 - Configure Kubernetes Client

* [Manual Setup](/kubam/stage4/manual)
