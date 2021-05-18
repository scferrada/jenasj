import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


flann = []
vp = []
bf = []

for line in open("flann.res"):
	if line.startswith("1"):
		parts = line.split(",")
		flann.append((int(parts[1]),int(parts[2]), float(parts[3].strip())))
		
for line in open("vp.res"):
	if line.startswith("1"):
		parts = line.split(",")
		vp.append((int(parts[1]),int(parts[2]), float(parts[3].strip())))
		
for line in open("bf.res"):
	if line.startswith("1"):
		parts = line.split(",")
		bf.append((int(parts[1]),int(parts[2]), float(parts[3].strip())))

flann.sort(key=lambda x:x[0])
fprop = np.array([x[0] for x in flann])
fent = np.array([x[1] for x in flann])
ftime = np.array([x[2] for x in flann])

vp.sort(key=lambda x:x[0])
vprop = np.array([x[0] for x in vp])
vent = np.array([x[1] for x in vp])
vtime = np.array([x[2] for x in vp])

bf.sort(key=lambda x:x[0])
bprop = np.array([x[0] for x in bf])
bent = np.array([x[1] for x in bf])
btime = np.array([x[2] for x in bf])

df1 = pd.DataFrame(np.vstack((fprop,ftime,)).T, columns=["Properties","Execution Time"]).assign(Algorithm="FLANN")
df2 = pd.DataFrame(np.vstack((vprop,vtime)).T, columns=["Properties","Execution Time"]).assign(Algorithm="VP-TREE")
df3 = pd.DataFrame(np.vstack((bprop,btime)).T, columns=["Properties","Execution Time"]).assign(Algorithm="NESTED LOOP")

cdf = pd.concat([df1, df2, df3])


fig, ax = plt.subplots(figsize=(8,4))
#ax = 
sns.boxplot(data=cdf, x="Properties", y="Execution Time", hue="Algorithm", palette="muted", width=0.7)#, ax=ax)
fig.get_axes()[0].set_yscale('log')
#sns.boxplot(x=fprop, y=ftime)#, ax=ax)
#ax.scatter(fent, fprop, s=np.sqrt(ftime), label='FLANN', alpha=0.5)
#ax.scatter(vent, vprop, s=np.sqrt(vtime), label='VP', alpha=0.5)
#ax.boxplot(np.concatenate((vprop, vtime)))#, '-x', label='VP-TREE', alpha=0.5)
#ax.boxplot(np.concatenate((fprop, ftime)))#, '-^', label='FLANN', alpha=0.5)


ax.set(xlabel='# of Properties', ylabel='Execution Time (secs.)',
       title=r'Execution Time Distribution by # of Properties. $k=1$')

#ax.legend()
#fig.tight_layout()
fig.savefig("box1.png")
plt.show()