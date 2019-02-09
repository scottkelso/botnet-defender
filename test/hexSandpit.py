import pandas as pd


def convert(x):
    try:
        val = int(x)
    except ValueError:
        try:
            val = int(x, 16)
        except ValueError:
            val = -2
    return val


d = {'Dport': ['http', '0x0adb', '8883', '-1'], 'Sport': ['33129', '0x0008', '35896', '-1']}
data = pd.DataFrame(d)

# if number -> int
# else if hex -> int
#      else -> val / encode

fin = data.applymap(convert)
