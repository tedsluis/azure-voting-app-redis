# Voting App

This sample creates 3 variants of a multi-container application for a Kubernetes cluster. The application interface has been built using Python / Flask. The data component is using Redis.

## App variants

|App variant |image name               | number of buttons | directory   | image port & path | docker-compose port & path |
---------------------------------------------------------------------------------------------------------------------------
| Vote       |tedsluis/vote-front      | 2                 | vote/       | :8090/vote        | :80/vote                   |
| Reset      |tedsluis/vote-reset-front| 3                 | vote-reset/ | :8090/reset       | :80/reset                  |
| Multi      |tedsluis/vote-multi-front| 0-5               | vote-multi/ | :8070/multi       | :80/multi                  |
 
## Steps

* Build images
* Run images locally and test apps
* Push images to a container registry
* Deploy apps on Kubernetes

## Build images
  
This step is opional. If you just want to deploy the apps on Kubernetes, you can use my images that I pushed to Docker Hub.  
  
Prerequisites:
* Linux host with Docker & Docker compose installed
* Internet connectivity (including access to Docker Hub)
* Clone this repo  
  
To build images locally and start containers via Docker-compose:
```
$ ./rebuild.sh
Stopping vote-reset-front ... done
Stopping vote-multi-front ... done
Stopping vote-back        ... done
Stopping vote-front       ... done
Removing vote-reset-front ... done
Removing vote-multi-front ... done
Removing vote-back        ... done
Removing vote-front       ... done
Removing network voting-app-redis_default
vote-back uses an image, skipping
Building vote-reset-front
Building vote-front
Building vote-multi-front
Creating network "voting-app-redis_default" with the default driver
Creating vote-front       ... done
Creating vote-back        ... done
Creating vote-reset-front ... done
Creating vote-multi-front ... done

$ sudo docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                           NAMES
15141632acd5        vote-reset-front    "/entrypoint.sh /s..."   21 minutes ago      Up 21 minutes       443/tcp, 0.0.0.0:8080->80/tcp   vote-reset-front
3fe74152db35        vote-multi-front    "/entrypoint.sh /s..."   21 minutes ago      Up 21 minutes       443/tcp, 0.0.0.0:8070->80/tcp   vote-multi-front
7dd299d01506        vote-front          "/entrypoint.sh /s..."   21 minutes ago      Up 21 minutes       443/tcp, 0.0.0.0:8090->80/tcp   vote-front
e260a14b9064        redis               "docker-entrypoint..."   21 minutes ago      Up 21 minutes       0.0.0.0:6379->6379/tcp          vote-back
```
The apps will be started after a successfull build.
  
## Test the apps locally
  
Try the URLs below in a webbrowser on the same system:

* http://localhost:8070/multi
* http://localhost:8080/reset
* http://localhost:8090/vote

Or use curl http://\<url\> from the commandline. 
  
## Tag and push the images to a container registry (Docker Hub or ACR)
  
Login to your container registry, for example to Docker hub:
```
$ docker login --username tedsluis --password <password>
```
  
To tag and push images:  
(be sure edit the namespace tag in the *tag_and_push.sh* script!)   
```
$ ./tag_and_push.sh 
The push refers to a repository [docker.io/tedsluis/vote-front]
The push refers to a repository [docker.io/tedsluis/vote-reset-front]
The push refers to a repository [docker.io/tedsluis/vote-multi-front]

$ sudo docker images | grep vote | grep v1
tedsluis/vote-multi-front              v1                  70d73e55bc1a        19 minutes ago      945 MB
tedsluis/vote-front                    v1                  a6b8787e7904        About an hour ago   945 MB
tedsluis/vote-reset-front              v1                  a6b8787e7904        About an hour ago   945 MB
```


