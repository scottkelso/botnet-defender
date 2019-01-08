from utils.reader import packetizer
from collections import OrderedDict
from utils.pcap_utils import get_ip_port
from utils.packet_helper import is_protocol, is_external
import numpy as np

packet_dict = packetizer("data/IoT_Dataset_OSScan__00001_20180521140502.pcap")
# grouped_packets = group_by_device("data/IoT_Dataset_OSScan__00001_20180521140502.pcap")


# Go through the packets one by one and add them to the session dict
print("Grouping " + str(len(packet_dict.items())) + " packets by device...")
working_dict = OrderedDict()

for head, packet in packet_dict.items():
    datetime = head[0]
    src = head[1]
    dst = head[2]

    if src not in working_dict:
        working_dict[src] = []

    working_dict[src].append((datetime, dst, packet))


print("Extracting features from " + str(len(working_dict.items())) + " devices...")
max_port = 1024
X = []
y = []
assigned_labels = []
for src, data in working_dict.items():

    # Initialize some counter variables
    num_src_port = [0] * max_port
    num_dst_port = [0] * max_port

    num_packets = 0
    num_external = 0
    num_tcp_sess = 0
    num_udp_sess = 0
    num_icmp_sess = 0

    datetime = data[0]
    dst = data[1]
    packets = data[2]

    src_address, src_port = get_ip_port(src)

    for record in packets:
        dst_address, dst_port = get_ip_port(dst)
        
        num_packets += 1
        num_external += is_external(src_address, dst_address)
        num_tcp_sess += is_protocol(record, '06')
        num_udp_sess += is_protocol(record, '11')
        num_icmp_sess += is_protocol(record, '01')
        
        if int(src_port) < max_port:
            num_src_port[int(src_port)] += 1

        if int(dst_port) < max_port:
            num_dst_port[int(dst_port)] += 1

    extra_features = [0] * 4
    extra_features[0] = num_external / num_packets
    extra_features[1] = num_tcp_sess / num_packets
    extra_features[2] = num_udp_sess / num_packets
    extra_features[3] = num_icmp_sess / num_packets
        
    feature_vector = np.concatenate(
        (
            num_packets,
            num_external,
            num_tcp_sess,
            num_udp_sess,
            num_icmp_sess,
            num_src_port,
            num_dst_port,
            extra_features
        ), 
        axis=0
    )
        
    X.append(feature_vector)
    y.append("Reconnaissance")
