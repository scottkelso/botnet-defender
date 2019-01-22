#!/bin/bash

##### POSTREQUISITS #####

# Run mininet topology
mn --topo single,10 --mac --controller=remote,ip=$DOCKER_HOST,port=6653 --controller=remote,ip=$DOCKER_HOST,port=6654 --switch ovsk


# Capture traffic on mirror port 10
timeout 5s tcpdump -w /traffic/capture/file.pcap -i h10-eth0
argus -i h10-eth0 -P 561 -d -w /traffic/capture/test.argus
ra -L 0 -r /traffic/capture/test.argus -s stime,flgs,proto,saddr,sport,dir,daddr,dport,pkts,bytes,state,srcid,ltime,seq,dur,mean,stddev,smac,dmac,sum,min,max,soui,doui,sco,dco,spkts,dpkts,sbytes,dbytes,rate,srate,drate, > /traffic/capture/test.argus.ascii.csv
ra -S 10.0.0.10:561 -s stime,flgs,proto,saddr,sport,dir,daddr,dport,pkts,bytes,state,srcid,ltime,seq,dur,mean,stddev,smac,dmac,sum,min,max,soui,doui,sco,dco,spkts,dpkts,sbytes,dbytes,rate,srate,drate > /traffic/capture/test.argus.ascii.csv

# Replay traffic on host
tcpreplay -i h5-eth0 -x 0.7 -l 3 --unique-ip /traffic/some.pcap
