#!/bin/bash

##### PREREQUISITS #####

# ~/Documents/csc4006/docker-mininet
# ~/Documents/csc4006/traffic
# docker & docker group
# (https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user)
# assuming that faucet directories have been setup

# Grab local IP address
ip=`hostname -I | awk '{print $1}'`
echo "Using $ip as host IP address"
echo "Ensure this is correct to allow mininet to conect to the faucet and gauge controllers"
echo "Can be omitted for machines with static ip address\n"

# Add permissions for mininet's xterms on the host machine
sudo xhost +

# Run Mininet
cd ~/Documents/csc4006/docker-mininet
docker build -t mininet .
#docker build --no-cache -t mininet .
docker run -it --rm --privileged \
            -e DISPLAY -e DOCKER_HOST=$ip \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            -v /lib/modules:/lib/modules \
            -v ~/Documents/csc4006/traffic:/traffic/ \
            -v ~/Documents/csc4006/botnet-defender/netUtils/:/utils/ mininet


##### POSTREQUISITS #####

# # Run mininet topology
# mn --topo single,10 --mac --controller=remote,ip=$DOCKER_HOST,port=6653 --controller=remote,ip=$DOCKER_HOST,port=6654 --switch ovsk
