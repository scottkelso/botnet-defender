def extract_macs(packet):
    '''
    Takes in hex representation of a packet header and extracts the
    source and destination mac addresses

    returns:
        source_mac: Destination MAC address
        destination_mac: Destination MAC address
    '''

    source_mac = packet[12:24]
    dest_mac = packet[0:12]

    source_mac = ':'.join(source_mac[i:i+2]
                          for i in range(0, len(source_mac), 2)
                          )
    destination_mac = ':'.join(dest_mac[i:i+2]
                               for i in range(0, len(dest_mac), 2)
                               )

    return source_mac, destination_mac


def packet_size(packet):
    '''
    Extracts the size of a packet in bytes from the hex header.

    Args:
        packet: Hex header of the packet

    Returns:
        size: Size in bytes of the IP packet, including data
    '''

    size = packet[1][32:36]
    try:
        size = int(size, 16)
    except Exception as e:
        size = 0

    return size


def extract_device_packet_size(device_packets):
    '''
    Extracts the total size of a session in bytes.

    Args:
        device_packets: session list containing all the packets of the session

    Returns:
        total_size: Size of the session in bytes
    '''

    total_size = sum([packet_size(p) for p in device_packets])
    return total_size


def extract_protocol(record):
    '''
    Extracts the protocol used in the session from the first packet

    Args:
        record: (datetime, dst, data)

    Returns:
        protocol: Protocol number used in the packet
    '''

    protocol = record[2][46:48]
    return protocol


def is_protocol(session, protocol):
    '''
    Checks if a session is of the type specified

    Args:
        session: List of packets in the session
        protocol: Protocol to check

    Returns:
        is_protocol: True or False indicating if this is a TCP session
    '''

    p = extract_protocol(session)
    if protocol == p:
        return True
    return False


def is_external(address_1, address_2):
    '''
    Checks if a session is between two sources within the same network.
    For now this is defined as two IPs with the first octet matching.

    Args:
        address_1: Address of source participant
        address_2: Address of destination participant

    Returns:
        is_external: True or False if this is an internal session
    '''

    if is_private(address_1) and is_private(address_2):
        return False

    return True


def is_private(address):
    '''
    Checks if an address is private and if so returns True.  Otherwise returns
    False.
    Args:
        address: Address to check. Can be list or string
    Returns:
        True or False
    '''
    if '.' in address:  # ipv4
        pairs = address.split('.')
    elif ':' in address:  # ipv6
        pairs = address.split(':')
    else:  # unknown
        pairs = []

    private = False
    if pairs:
        if pairs[0] == '10':
            private = True
        elif pairs[0] == '192' and pairs[1] == '168':
            private = True
        elif pairs[0] == '172' and 16 <= int(pairs[1]) <= 31:
            private = True
        elif pairs[0] == 'fe80':
            private = True
        elif pairs[0].startswith('fd'):
            private = True

    return private