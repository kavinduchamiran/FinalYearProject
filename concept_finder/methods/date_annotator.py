"""
try to figure out concept of different date type columns using a parser and label the column based on 
heuristic of subject column concept 
"""

def findDateConcept(subject_concept, sample_value_sets):
    with open('./datasets/numerical_data/domainToDate.json') as f:
        domain_to_dates = json.load(f)

    if subject_concept == "http://dbpedia.org/ontology/VideoGame":
        if len(sample_value_sets) == 1 and isYear(sample_value_sets[0]):
            return [domain_to_dates[subject_concept][0]]
        else: 
            return [domain_to_dates[subject_concept][1]]
    elif subject_concept == "http://dbpedia.org/ontology/BaseballPlayer":
            if len(sample_value_sets) == 2:
                return domain_to_dates[subject_concept]
            else:
                return None
    elif subject_concept == "http://dbpedia.org/ontology/Country":
        if len(sample_value_sets) == 1:
            return [domain_to_dates[subject_concept][1]]
    
    elif subject_concept == "http://dbpedia.org/ontology/Person":
            if len(sample_value_sets) == 2:
                return domain_to_dates[subject_concept]
            else:
                return None
    # for other cases having only one date type
    return domain_to_dates[subject_concept][0]

def isYear(value_set):
    count = 0 
    for v in value_set:
        if len(v) == 4:
            count += 1
    if float(count)/float(len(value_set)) > 0.75:
        return True
    else:
        return False


# print(findDateConcept("http://dbpedia.org/ontology/VideoGame", [['2011', '2010', '2004', 'asfasfs']]))
# print(findDateConcept("http://dbpedia.org/ontology/Person", [['19.11.1912', '20.05.1822', '23.04.1897', '30.09.1870'], ['19.11.1912', '20.05.1822', '23.04.1897', '30.09.1870']]))
# print(findDateConcept("http://dbpedia.org/ontology/Building", [['19.11.1912', '20.05.1822', '23.04.1897', '30.09.1870']]))











