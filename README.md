# botnet-defender
A proposed botnet detector tailored towards Mirai-like botnets, uses machine learning to detect the preliminary stages and react to them in an SDN environment.

The system will consist of the following elements...
1. Mininet virtual network which can run traffic and capture live traffic, storing into the host machine
2. A python application which can grab those traffic files and run machine learning on them and then if action is required, edit the faucet.yaml file to enforce new flow rules for the SDN.

# Prerequisits
* [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce-1)
* [Faucet, Grafana, Prometheus](https://faucet.readthedocs.io/en/latest/tutorials/first_time.html)
* [Mininet](http://mininet.org)
* [Python](https://www.python.org/)

# Setup Guide
* Install [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce-1)
* [Add sudo privileges](https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user) to docker
* Install [Faucet, Grafana, Prometheus & Guage](https://faucet.readthedocs.io/en/latest/tutorials/first_time.html)
* Download and build [custom mininet docker container](https://github.com/scottkelso/docker-mininet)
(See `./mininet.sh`)

# Related Work
* https://github.com/scottkelso/sdn-security
* https://github.com/a-blaise/split-and-merge
* https://github.com/CyberReboot/PoseidonML
* https://github.com/CyberReboot/poseidon
* https://github.com/ianwelch/faucet-bro/

# Data
* http://mawi.wide.ad.jp/mawi/samplepoint-F/2016/
* https://www.unsw.adfa.edu.au/unsw-canberra-cyber/cybersecurity/ADFA-NB15-Datasets/bot_iot.php
