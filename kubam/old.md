---
layout: page
title: KUBAM! Under the magic!
tags: Kubernetes, containers
---
{% include JB/setup %}

We started building KUBAM as a recipe book, then scripts, and finally into the simplified version that is available today.  Each time we built something we said:  "That is too complicated!  Simplify it!".  And so we did, and we keep doing that.  But, we left some history here, so you can get an idea of what the code is actually doing.  If you are the person that likes to play at home, this is perhaps the place for you to start!

We first divided a hard problem into multiple steps and our first project was Kubernetes.  That's what you will see here in the old docs. 

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
