import os

dimensions = {}

for p,d,f in os.walk("sparql"):
	for file in f:
		reader = open(os.path.join(p,file))
		select = reader.readline()
		select = reader.readline()
		parts = select.split("?")
		if file not in dimensions:
			dimensions[file] = []
		dimensions[file].append(len(parts)-1)
		reader.close()
		
for p,d,f in os.walk("out/flann/1"):
	for file in [x for x in f if x.endswith("1")]:
		nb_lines = len(open(os.path.join(p,file)).readlines())
		dimensions[file[:-1]].append(nb_lines)

with open("dim.txt", "w") as out:
	for k in dimensions:
		txt = "%s, %d, %d\n" % (k[:k.index(".")+1], dimensions[k][0], dimensions[k][1])
		out.write(txt)