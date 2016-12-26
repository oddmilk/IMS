# element-wise string concatenation
import numpy as np 

s = ","
test = s.join(titles)

import re 
p0 = re.compile(Tag[0])
c0 = re.findall(p0, test)
len(c0)


p1 = re.compile(Tag[1])
c1 = re.findall(p1, test)
len(c1)


p2 = re.compile(Tag[2])
c2 = re.findall(p2, test)
len(c2)


p3 = re.compile(Tag[3])
c3 = re.findall(p3, test)
len(c3)


p4 = re.compile(Tag[4])
c4 = re.findall(p4, test)
len(c4)

p5 = re.compile(Tag[5])
c5 = re.findall(p5, test)
len(c5)

p6 = re.compile(Tag[6])
c6 = re.findall(p6, test)
len(c6)

p7 = re.compile(Tag[7])
c7 = re.findall(p7, test)
len(c7)

p8 = re.compile(Tag[8])
c8 = re.findall(p8, test)
len(c8)

p9 = re.compile(Tag[9])
c9 = re.findall(p9, test)
len(c9)


p = []
c = [len(c1), len(c2), len(c3), len(c4), len(c5), len(c6), len(c7), len(c8), len(c9)]

for i in range(len(Tag)):
	p[i] = re.compile(Tag[i])
	c[i] = len(re.findall(p[i], test))
	print(c[i])

