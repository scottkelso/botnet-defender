#!/usr/bin/env bash

captureWindow=15
captureDir="/traffic/capture/"

# Start argus server on host 10's port 561
argus -i h10-eth0 -P 561 -d -w /traffic/capture/capture.argus

count=0
while true
do
  count=$((count+1))
  datetime=`date '+%Y-%m-%d_%H-%M-%S'`
  filename="$captureDir$datetime.argus.csv"

  # Capture traffic for captureWindow seconds and output to filename
  ra -S 10.0.0.10:561 -L 0 -c ';' -T ${captureWindow} -s stime flgs proto saddr sport dir daddr dport pkts bytes state srcid ltime seq dur mean stddev smac dmac sum min max soui doui sco dco spkts dpkts sbytes dbytes rate srate drate > ${filename}
  echo "[$count] $captureWindow second capture saved: $filename"
done
