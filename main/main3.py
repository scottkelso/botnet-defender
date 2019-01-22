from utils.reader import packetizer
from collections import OrderedDict
from utils.pcap_utils import get_ip_port
from utils.packet_helper import is_protocol, is_external, extract_macs
import numpy as np

print("Launching packetizer...")
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

    for record in data:

        datetime = record[0]
        dst = record[1]
        packets = record[2]

        # CSV's have all ['smac', 'dmac'] as 'nan'

        # src_mac, dst_mac = extract_macs(record[2])
        # src_address, src_port = get_ip_port(src_mac)
        # dst_address, dst_port = get_ip_port(dst_mac)
        
        num_packets += 1
        # num_external += is_external(src_address, dst_address)
        num_tcp_sess += is_protocol(record, '06')
        num_udp_sess += is_protocol(record, '11')
        num_icmp_sess += is_protocol(record, '01')
        
        # if int(src_port) < max_port:
        #     num_src_port[int(src_port)] += 1
        #
        # if int(dst_port) < max_port:
        #     num_dst_port[int(dst_port)] += 1

    extra_features = [0] * 4
    extra_features[0] = num_external / num_packets
    extra_features[1] = num_tcp_sess / num_packets
    extra_features[2] = num_udp_sess / num_packets
    extra_features[3] = num_icmp_sess / num_packets

    # num_ports = np.concatenate(
    #     (
    #         num_src_port,
    #         num_dst_port,
    #     ),
    #     axis=0
    # )
        
    # feature_vector = np.concatenate(
    #     (
    #         np.asarray(num_ports),
    #         extra_features
    #     ),
    #     axis=0
    # )
        
    X.append(extra_features)
    y.append('Reconnaissance')
    # This is no good for training - we don't know ground truth
    # Therefore use CSV
