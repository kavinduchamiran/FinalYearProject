import os
import pickle

with open('grouped.pkl', 'rb') as f:
    files = pickle.load(f)

with open('results a.txt', 'r') as r:
    res = r.read().split('\n')
    results = {}

    for i in res:
        j = i.split(' ')
        results[j[0] + '.csv'] = map(int, tuple(j[1:]))

with open('ne_li_count.txt', 'r') as r:
    res = r.read().split('\n')
    count = {}

    for i in res:
        j = i.split(' ')
        count[j[0] + '.csv'] = list(map(int, tuple(j[1:])))

def get_summary(l):
    tp, fp, fn, ne, li, ne_t, li_t = 0,0,0,0,0,0,0
    for r in l:
        for f in files[r]:
            tp1, fp1, fn1, ne1, li1 = results[f]
            tp += tp1
            fp += fp1
            fn += fn1
            ne += ne1
            li += li1

            ne_t += count[f][0]
            li_t += count[f][1]

    return (tp, fp, fn, ne, li, ne_t, li_t)

def get_metrics(tp, fp, fn):
    if tp == 0 and fp == 0:
        P = 0
    else:
        P = tp / float(tp + fp) * 100

    if tp == 0 and fn == 0:
        R = 0
    else:
        R = tp / float(tp + fn) * 100

    if P == 0 and R == 0:
        F1 = 0
    else:
        F1 = 2 * P * R / (P + R)

    return P, R, F1


tp, fp, fn, ne, li, ne_t, li_t = get_summary(['ArchitecturalStructure', 'NaturalPlace', 'Organisation', 'Person', 'PopulatedPlace', 'Species', 'Work'])
print(float(ne*100)/ne_t, float(li*100)/li_t)

print(get_metrics(tp,fp,fn))




