---
layout: page
title: KUBaM! - Kubernetes on UCS Bare Metal
tags: Kubernetes, containers
---
{% include JB/setup %}

 
<div class="alert alert-warning">
This is a <b>WORK IN PROGRESS</b>.  We are building the airplane while its in the air.  If you've stumbled upon this page then please know that we are in pre-Alpha mode!
</div>

Hello! Shalom! Aloha!  Hola! Ciao!

Welcome to KUBaM! You have UCS and you want Kubernetes running on it as fast as possible. Before you can even say KUBaM we will make that happen.  There are a few steps you'll need to do, and we are constantly improving this process to make those steps even less.

You may also have ways you like doing things with your tools.  Therefore, in each stage we have and will continue to add options of how each stage can be accomplished.  Have a tool?  [Let us know](http://twitter.com/vallard) and we'll prioritize it. 

Installing Kubernetes on UCS Bare Metal is a 4 stage process.   At each stage you may have several options and we will add options as they become available.  
## Stage 1 - Prepare 
You will need a management server that has all the bits required for the kubernetes setup.

* [Manual Preparation](/kubam/stage1/manual)

## Stage 2 - UCS Bare Metal Deployment

In this stage you will need to setup UCS service profiles in a way so they automatically install the operating system. 

* [UCSM Python Scripts](/kubam/stage2/python)

## Stage 3 - Install Kubernetes

Here we automate the installation process of Kubernetes on operating systems that are now provisioned. 

* [Ansible Scripts](/kubam/stage3/ansible)

## Stage 4 - Configure Kubernetes Client

* [Manual Setup](/kubam/stage4/manual)
