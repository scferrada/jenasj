flann = {}
vp = {}

for line in open("flann.res"):
	parts = line.split(",")
	if (int(parts[0]),int(parts[1]), int(parts[2])) in flann:
		if float(parts[3].strip()) < flann[(int(parts[0]),int(parts[1]), int(parts[2]))]:
			flann[(int(parts[0]),int(parts[1]), int(parts[2]))] =  float(parts[3].strip())
			continue
	flann[(int(parts[0]),int(parts[1]), int(parts[2]))] =  float(parts[3].strip())
		
for line in open("vp.res"):
	parts = line.split(",")
	vp[(int(parts[0]),int(parts[1]), int(parts[2]))] =  float(parts[3].strip())
	
wf = 0
wv = 0	
tie = 0
print(len(flann))
print(len(vp))
	
for k in flann:
	if flann[k] < vp[k]:
		wf+=1
	elif vp[k] < flann[k]:
		wv+=1
	else:
		tie +=1
		
print("flann: %d\nVP: %d"%(wf, wv))
print(tie)