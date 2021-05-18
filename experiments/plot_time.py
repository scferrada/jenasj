import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from scipy.interpolate import make_interp_spline, BSpline

flann = []
vp = []
bf = []

for line in open("flann.res"):
	if line.startswith("1"):
		parts = line.split(",")
		flann.append((int(parts[2]), float(parts[3].strip())))
		
for line in open("vp.res"):
	if line.startswith("1"):
		parts = line.split(",")
		vp.append((int(parts[2]), float(parts[3].strip())))
		
for line in open("bf.res"):
	if line.startswith("1"):
		parts = line.split(",")
		bf.append((int(parts[2]), float(parts[3].strip())))

flann.sort(key=lambda x:x[0])
t1 = np.array([x[0] for x in flann])
s1 = np.array([x[1] for x in flann])

vp.sort(key=lambda x:x[0])
t2 = np.array([x[0] for x in vp])
s2 = np.array([x[1] for x in vp])

bf.sort(key=lambda x:x[0])
t3 = np.array([x[0] for x in bf])
s3 = np.array([x[1] for x in bf])

fig, ax = plt.subplots(figsize=(8,4))

df1 = pd.DataFrame(np.vstack((np.floor_divide(t1,500)*500,s1)).T, columns=["ents","time"])
df1.groupby("ents").mean()["time"].plot(marker='o', alpha=0.6, label="FLANN")

df2 = pd.DataFrame(np.vstack((np.floor_divide(t2,500)*500,s2)).T, columns=["ents","time"])
df2.groupby("ents").mean()["time"].plot(marker='^', alpha=0.6, label="VP-TREE")

df3 = pd.DataFrame(np.vstack((np.floor_divide(t3,500)*500,s3)).T, columns=["ents","time"])
df3.groupby("ents").mean()["time"].plot(marker='s', alpha=0.6, label="NESTED LOOP", logy=True)
#ax.plot(x=df2["ents"], y=(df2["ents"]*np.log2(df2["ents"])), alpha=0.4, label=r"$n\log n$")



#tnew1 = np.linspace(t1.min(), t1.max(), 300)
#spl = make_interp_spline(t1, s1, k=3)
#s1_smooth =  spl(tnew1)

#ax.plot(tnew1, s1_smooth, '--', label='FLANN')
#ax.plot(t2, s2, ':', label='VP-TREE')

ax.set(xlabel='# of Entities', ylabel='Execution Time (secs.)',
       title=r'Execution times for $k=1$')

ax.legend()
fig.savefig("k1.png")
plt.show()