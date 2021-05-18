import os

dimensions = {}
for line in open("dim.txt"):
	parts = line.split(",")
	dimensions[parts[0]]=(int(parts[1].strip()), int(parts[2].strip()))
	
res = {}	
for p,d,f in os.walk("out/bf"):
	print(p)
	for file in [x for x in f if x.endswith("time")]:
		k = int(p[-1])
		line = open(os.path.join(p, file)).readline().translate(str.maketrans('','','[]'))
		parts = line.split(",")
		time = sum([float(x.strip()) for x in parts])/len(parts)
		query = file[:file.index(".")]
		if query not in res:
			res[query] = []
		res[query].append([dimensions[query][0], dimensions[query][1], k, time])
		
with open("bf.res", "w") as out:
	for q in res:
		for l in res[q]:
			txt = "%d,%d,%d,%s\n" % (l[2], l[0], l[1], str(l[3]))
			out.write(txt)