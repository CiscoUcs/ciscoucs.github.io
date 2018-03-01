# KUBAM Installation

The base KUBAM requires a dedicated server that can either be physical or virtual.  We recommend a virtual machine with the following requirements

| Description | Requirement |
| ----------- | ----------- |
| RAM         | 4-8GB       |
| HD Space    | 20GB        |
| OS          | Linux based |

KUBAM has been tested with Ubuntu, CoreOS, and RedHat derivatives. 

We recommend you install KUBAM as a container as this is the fastest and easiest way to get updates.  It also avoids dependency hell.

Nevertheless we know there are many use cases where people want to install KUBAM in different ways.  Therefore we have included ways to install without using a docker container.  This installation method requires only minimal configuration and tweaking.

![will it work](https://imgs.xkcd.com/comics/will_it_work.png)