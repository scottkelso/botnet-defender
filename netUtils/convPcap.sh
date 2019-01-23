#!/usr/bin/env bash

if (( $# > 0 )); then

    file=$1
    argusFile="$file.argus"
    csvFile="$file.csv"

    # Start argus server on input file
    argus -r ${file} -w ${argusFile}

    # Capture traffic output to csv
    ra -r ${argusFile} -L 0 -c ';' -s stime flgs proto saddr sport dir daddr dport pkts bytes state srcid ltime seq dur mean stddev smac dmac sum min max soui doui sco dco spkts dpkts sbytes dbytes rate srate drate > ${csvFile}

else
    echo "USAGE: bash convPcap.sh <inputfile>"
fi
