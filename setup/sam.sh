#!/usr/bin/env bash

# Some notes on how one might compile and run SPLIT-AND-MERGE (SAM)
# Use requirements.txt

#http://libtins.github.io/download/
git clone https://github.com/mfontanini/libtins.git
cd libtins

apt-get install libpcap-dev libssl-dev cmake

mkdir build
cd build
cmake ../
make

make install


cd ../../
#https://github.com/a-blaise/split-and-merge
git clone https://github.com/a-blaise/split-and-merge.git
cd split-and-merge

pip install pandas numpy scipy matplotlib

cd generate_csvs/
mkdir build
cd build
cmake ../
make
./get_csvs
