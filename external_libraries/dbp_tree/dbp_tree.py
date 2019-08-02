from anytree import Node, RenderTree
import urllib3
from bs4 import BeautifulSoup as bs

http = urllib3.PoolManager()
uri = 'http://mappings.dbpedia.org/server/ontology/classes/'
req = http.request('GET', uri)

if req.status == 200:
    soup = bs(req.data, "html.parser")
    soup.prettify()

    root = soup.body.ul.li
    print(root.a['name'])

#     meke ituru tika gahapan puluwan nam
# traverse karala tree object ekak return wenna
# anytree eke documentation balapan

