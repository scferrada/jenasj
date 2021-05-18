import os

for p,d,f in os.walk('sp2'):
	for file in f:
		with open(os.path.join(p, file), 'r+') as wr:
			txt = wr.read()
			txt = txt.replace(',', ' ')
			wr.seek(0)
			wr.write(txt)
			wr.truncate()