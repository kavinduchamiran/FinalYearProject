import urllib3
import json
import pprint

def query_dbpedia_lookup_endpoint(entity_label):
    """
    query dbpedia lookup endpoint for an entity information
    :param entity_label: the label of the entity eg: usa or sri lanka
    :return: list: set of dicts {label: dbo:uri} the classes the entity might belong to
    """
    url = 'http://lookup.dbpedia.org/api/search/KeywordSearch?MaxHits=1&QueryString=%s' % entity_label
    http = urllib3.PoolManager()

    req = http.request('GET', url, headers={'Accept': 'application/json'})

    json_data = json.loads(req.data.decode('utf-8'))

    if json_data['results']:
        results = json_data['results'][0]['classes']
        return [result['uri'][28:] for result in results if 'http://dbpedia.org/ontology' in result['uri']]
    return []


