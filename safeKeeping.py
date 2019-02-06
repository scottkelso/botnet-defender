# # Drop all ipv6 and icmp packets
# df = df[~df.proto.str.contains("ipv6", na=False)]
# df = df[~df.proto.str.contains("icmp", na=False)]
#
# # https://en.wikipedia.org/wiki/Xinetd
# df = df[~df.sport.str.contains("xinetd", na=False)]
#
# # https://networkupstools.org/docs/user-manual.chunked/ar01s09.html
# df = df[~df.dport.str.contains("nut", na=False)]
#
# # Reset indexes that now have missing values
# df = df.reset_index(drop=True)














# # Drop all ipv6, icmp & llc packets
# df = df[~df.Proto.str.contains("ipv6", na=False)]
# df = df[~df.Proto.str.contains("icmp", na=False)]
# df = df[~df.Proto.str.contains("llc", na=False)]
# df = df[~df.Proto.str.contains("man", na=False)]
#
# # TODO(jk): Make ports null or negative number represented instead of dropping record
#
# # https://en.wikipedia.org/wiki/Xinetd
# df = df[~df.Sport.str.contains("xinetd", na=False)]
#
# # https://networkupstools.org/docs/user-manual.chunked/ar01s09.html
# df = df[~df.Dport.str.contains("nut", na=False)]
#
# df = df[~df.Sport.str.contains("domain", na=False)]
# df = df[~df.Dport.str.contains("domain", na=False)]
#
# df = df[~df.Sport.str.contains("bootpc", na=False)]
# df = df[~df.Dport.str.contains("bootps", na=False)]
# df = df[~df.Sport.str.contains("bootps", na=False)]
# df = df[~df.Dport.str.contains("bootpc", na=False)]
#
# df = df[~df.Dport.str.contains("http", na=False)]
# df = df[~df.Dport.str.contains("ntp", na=False)]
# df = df[~df.Dport.str.contains("xmpp-client", na=False)]
# df = df[~df.Dport.str.contains("mdns", na=False)]
# df = df[~df.Dport.str.contains("imaps", na=False)]

# Amazon Echo
# Dport - domain, http, https, bootps, ntp
# Sport - domain, bootpc

# Aura Smart Sleep ensor
# Dport - xmpp-client, mdns

# Reset indexes that now have missing values
# df = df.reset_index(drop=True)














# os.shape
# (360348, 27)

# am.shape
# (8953, 26)

# os.columns
# Index(['stime', 'flgs', 'proto', 'saddr', 'sport', 'dir', 'daddr', 'dport',
#        'pkts', 'bytes', 'state', 'srcid', 'ltime', 'dur', 'mean', 'stddev',
#        'sum', 'min', 'max', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate',
#        'srate', 'drate', 'category'],
#       dtype='object')

# am.columns
# Index(['StartTime', 'Flgs', 'Proto', 'SrcAddr', 'Sport', 'Dir', 'DstAddr',
#        'Dport', 'TotPkts', 'TotBytes', 'State', 'SrcId', 'LastTime', 'Dur',
#        'Mean', 'StdDev', 'Sum', 'Min', 'Max', 'SrcPkts', 'DstPkts', 'SrcBytes',
#        'DstBytes', 'Rate', 'SrcRate', 'DstRate'],
#       dtype='object')



# StartTime     object
# Flgs          object
# Proto         object
# SrcAddr       object
# Sport         object
# Dir           object
# DstAddr       object
# Dport         object
# TotPkts        int64
# TotBytes       int64
# State         object
# SrcId         object
# LastTime      object
# Dur          float64
# Mean         float64
# StdDev       float64
# Sum          float64
# Min          float64
# Max          float64
# SrcPkts        int64
# DstPkts        int64
# SrcBytes       int64
# DstBytes       int64
# Rate         float64
# SrcRate      float64
# DstRate      float64
# category      object








# check_types(data)
# <class 'str'>    1859906
# Name: Dir, dtype: int64
# <class 'str'>    1859906
# Name: Dport, dtype: int64
# <class 'str'>    1859906
# Name: DstAddr, dtype: int64
# <class 'int'>    1859906
# Name: DstBytes, dtype: int64
# <class 'int'>    1859906
# Name: DstPkts, dtype: int64
# <class 'float'>    1859906
# Name: DstRate, dtype: int64
# <class 'float'>    1859906
# Name: Dur, dtype: int64
# <class 'str'>    1859906
# Name: Flgs, dtype: int64
# <class 'float'>    1828321
# <class 'str'>        31585
# Name: LastTime, dtype: int64
# <class 'float'>    1859906
# Name: Max, dtype: int64
# <class 'float'>    1859906
# Name: Mean, dtype: int64
# <class 'float'>    1859906
# Name: Min, dtype: int64
# <class 'str'>    1859906
# Name: Proto, dtype: int64
# <class 'float'>    1859906
# Name: Rate, dtype: int64
# <class 'str'>    1859906
# Name: Sport, dtype: int64
# <class 'str'>    1859906
# Name: SrcAddr, dtype: int64
# <class 'int'>    1859906
# Name: SrcBytes, dtype: int64
# <class 'str'>    1859906
# Name: SrcId, dtype: int64
# <class 'int'>    1859906
# Name: SrcPkts, dtype: int64
# <class 'float'>    1859906
# Name: SrcRate, dtype: int64
# <class 'float'>    1828321
# <class 'str'>        31585
# Name: StartTime, dtype: int64
# <class 'str'>    1859906
# Name: State, dtype: int64
# <class 'float'>    1859906
# Name: StdDev, dtype: int64
# <class 'float'>    1859906