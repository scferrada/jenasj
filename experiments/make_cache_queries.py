import sys, os, random

query_template = '''
PREFIX wdt:<http://www.wikidata.org/prop/direct/>

SELECT ?id1 ?id2 ?d WHERE {
	{%s}
	SIMILARITY JOIN
	ON (%s) (%s)
	TOP 1
	USING 'manhattan' AS ?d
	
	{%s}
}
'''

for p,d,f in os.walk('./sparql'):
	for filename in f:
		print(filename)
		with open(os.path.join(p,filename), 'r') as query_file:
			p1 = []
			p2 = []
			current = p1
			for line in query_file:
				if line.endswith(';\n'):
					current.append(line.strip());
					continue
				if line.endswith('.\n'):
					current.append(line.strip())
					current=p2
					continue
			p1_txt = ''
			p1_vars = []
			for triple in p1:
				parts = triple.split()
				p1_vars.append(parts[-2])
				p1_txt += triple + '\n'
			p2_txt = ''
			p2_vars = []
			i = 0
			for triple in p2:
				parts = triple.split()
				p2_vars.append(parts[-2])
				p2_txt += triple + '\n'
				i+=1
			query = query_template % (p1_txt, ','.join(p1_vars), ','.join(p2_vars), p2_txt)
			with open(os.path.join('./sp2', filename), 'w') as out:
				out.write(query)
				