import random
import pickle
import os
import csv

# this file reads the triplets file and breaks into train.txt, test.txt and valid.txt
# it also generetes 2 pickle dics with {entity: id} and {relation: id}

try:
    files = ['train2id.txt', 'test2.id.txt', 'valid2id.txt', 'entity2id.txt', 'relation2id.txt', 'label_ent.pickle',
             'label_rel.pickle']
    for file in files:
        os.remove('./dataset/%s' % file)
except:
    pass

# cleaned version where sets only contain concepts in t2d
from external_libraries import helper_functions as hf
files = hf.iter_folder('./property/')

t2d_concepts = []
for file in files:
    lines = csv.reader(open('./property/' + file))
    for line in lines:
        t2d_concepts.append(line[0])

t2d_concepts = list(set(t2d_concepts))

data = open('../dbpedia_mappings/backup/dbr_dbo_dbr old.txt', 'r', encoding='utf8').read().split('\n')

data_tup = []

data = list(set(data))

for i in data:
    t = tuple(i.split('\t'))
    if t[1] in t2d_concepts:
        data_tup.append(t)

entities = []
entities_map = {}

relations = []
relations_map = {}

for (e1, r, e2) in data_tup:
    entities.append(e1)
    entities.append(e2)
    relations.append(r)

entities = list(set(entities))
relations = list(set(relations))

count = 0
for entity in entities:
    entities_map[entity] = count
    count += 1

count = 0
for relation in relations:
    relations_map[relation] = count
    count += 1

label_ent = {}  # open('./dataset/label_ent.txt', 'a+')
entity2id = open('./dataset/entity2id.txt', 'a+', encoding='utf8')

entity2id.write("{}\n".format(len(entities_map)))
for label, id in entities_map.items():
    label_ent[label] = id
    entity2id.write("{}\t{}\n".format(label, id))

with open('./dataset/label_ent.pickle', 'wb') as handle:
    pickle.dump(label_ent, handle, protocol=pickle.HIGHEST_PROTOCOL)

label_rel = {}  # open('./dataset/label_rel.txt', 'a+')
relation2id = open('./dataset/relation2id.txt', 'a+', encoding='utf8')

relation2id.write("{}\n".format(len(relations_map)))
for label, id in relations_map.items():
    label_rel[label] = id
    relation2id.write("{}\t{}\n".format(label, id))
with open('./dataset/label_rel.pickle', 'wb') as handle:
    pickle.dump(label_rel, handle, protocol=pickle.HIGHEST_PROTOCOL)

random.shuffle(data_tup)

total_records = len(data_tup)

# train, test, valid = 0.6, 0.2, 0.2

# train_end = int(total_records * train)
# test_end = train_end + int(total_records * test)
# valid_end = test2id + int (data_tup * 0.2)

train2id = open('./dataset/train2id.txt', 'a+', encoding='utf8')  # e1 \t e2 \t rel
# test2id = open('./dataset/test2id.txt', 'a+', encoding='utf8')  # e1 \t e2 \t rel
# valid2id = open('./dataset/valid2id.txt', 'a+', encoding='utf8')  # e1 \t e2 \t rel

train2id.write("{}\n".format(len(data_tup)))
for (e1, r, e2) in data_tup:
    train2id.write("{}\t{}\t{}\n".format(entities_map[e1], entities_map[e2], relations_map[r]))

# test2id.write("{}\n".format(len(data_tup[train_end: test_end])))
# for (e1, r, e2) in data_tup[train_end: test_end]:
#     test2id.write("{}\t{}\t{}\n".format(entities_map[e1], entities_map[e2], relations_map[r]))
#
# valid2id.write("{}\n".format(len(data_tup[test_end:])))
# for (e1, r, e2) in data_tup[test_end:]:
#     valid2id.write("{}\t{}\t{}\n".format(entities_map[e1], entities_map[e2], relations_map[r]))

# e1, e2, r for openke