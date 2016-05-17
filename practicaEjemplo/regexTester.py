regex = '(.*?) - - \[(.*?)\] "(.*?)" (\d+)'

line = '88.198.56.239 - - [26/Apr/2015:08:05:09 +0200] "GET a.html HTTP/1.1" 200'

line2 = '66-249-67-114 - - [26/Apr/2015:08:06:26 +0200] "GET b.html HTTP/1.1" 200 '

line3 = '48.251.124.42 - - [26/Apr/2015:08:12:36 +0200] "GET a.html HTTP/1.1" 200 '

line4  = '66-249-67-98 - - [26/Apr/2015:08:17:47 +0200] "GET a.html HTTP/1.1" 200 '

import re
print re.match(regex, line).groups()

print re.match(regex, line2).groups()

print re.match(regex, line3).groups()

print re.match(regex, line4).groups()