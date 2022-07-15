import re

# data = "crw-rw---- 1 root dialout 188, 0 Jul 15 08:40 /dev/ttyUSB0\n"
data = "ee"
match_data = re.findall("/dev/ttyUSB\d", data)
# match_data = re.match("/dev/ttyUSB", data)
print match_data
