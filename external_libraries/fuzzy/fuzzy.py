from fuzzywuzzy import fuzz
import re

# lines = open('../fast_text/training_data/train_fasttext3.txt', 'r').read().split('\n')
lines = open('../external_libraries/fast_text/training_data/train_fasttext3.txt', 'r').read().split('\n')
lines += open('../external_libraries/fast_text/training_data/train_fasttext2.txt', 'r').read().split('\n')

uris = []
labels = []

regex = re.compile(r'[a-zA-Z]+')

for line in lines:
    L = line.split(' ')
    uris.append(L[0])
    labels.append(L[1].lower())

n = len(lines)

def find_concept_fuzzy(label):
    # cleaning of table
    label = ''.join(regex.findall(label)).replace(' ', '').lower()

    curr = float('-inf')
    ans = ''
    for i in range(n):
        ratio = fuzz.ratio(label, labels[i])
        if ratio > curr:
            curr = ratio
            ans = uris[i]

    ans = 'http://dbpedia.org/ontology/' + ans[9:]
    return (ans, curr) if curr > 80 else (None, 0)


# print(find_concept_fuzzy('elevation'))