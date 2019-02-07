from sklearn.preprocessing import OneHotEncoder

X = [['tcp'], ['udp'], ['imcp']]
Y = [['tcp', 'nom'], ['udp', 'rec'], ['imcp', 'blah'], ['imcp', 'some']]
Z = [['tcp', 'kek'], ['ivp4', 'rec'], ['imcp', 'tot'], ['imcp', 'some']]
ZZ = [['tcp', 'kek', 6], ['ivp4', 'rec', 2], ['imcp', 'tot', 3], ['imcp', 'some', 3]]


# Encode all given categories but fails when transforming unknown category
enc = OneHotEncoder()
enc.fit(X)
out = enc.transform(X)
outarr = out.toarray()

# Encode all given categories
enc = OneHotEncoder(handle_unknown='ignore')
enc.fit(X)
out2 = enc.transform(X)
out2arr = out2.toarray()

enc.fit(ZZ)
out2 = enc.transform(ZZ)
out2arr = out2.toarray()

# Encode given categories and all other as one other encoding
enc = OneHotEncoder(handle_unknown='ignore', categories=[['tcp', 'udp']])
enc.fit(X)
out3 = enc.transform(X)
out3arr = out3.toarray()

# Encode given categories and all other as one other encoding
enc = OneHotEncoder(handle_unknown='ignore', categories=[['tcp', 'udp'], ['norm']])
enc.fit(Y)
out4 = enc.transform(Y)
out4arr = out4.toarray()

enc.fit(Z)
out5 = enc.transform(Z)
out5arr = out5.toarray()
