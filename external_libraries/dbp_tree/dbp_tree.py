"""
The concepts tree that results here contains class concepts only
"""

import urllib3
from bs4 import BeautifulSoup as bs

http = urllib3.PoolManager()
uri = 'http://mappings.dbpedia.org/server/ontology/classes/'
req = http.request('GET', uri)

if req.status == 200:
    soup = bs(req.data, "html.parser").body.ul
    s = []
    s.append(soup.find_all('li', recursive=False)[0]) 
    root = None
    with open('input.txt', 'a') as f:
        f.write("super owl:Thing\n")
        while len(s) > 0:
            parent = s[0].a['name']
            soup = s.pop(0).ul
            if soup is not None:
                items = soup.find_all('li', recursive=False)
                if items is not None:
                    for item in items:
                        s.append(item)
                        f.write(parent +" "+ item.a['name']+"\n")

print ("input.txt has been created! Run create_tree.py")