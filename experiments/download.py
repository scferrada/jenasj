import requests

url = "http://dumps.wikimedia.org/wikidatawiki/entities/latest-truthy.nt.bz2"
local_filename = "wikidata.nt.bz2"
    # NOTE the stream=True parameter below
with requests.get(url, stream=True) as r:
	r.raise_for_status()
	with open(local_filename, 'wb') as f:
		i = 0
		for chunk in r.iter_content(chunk_size=18192): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
				i += 1
				if i%100==0:
					print(i)