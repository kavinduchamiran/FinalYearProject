import random

source = open('./label_to_uri.txt').readlines()

dest = open('label_dbr.txt', 'a+')

# random.shuffle(source)

source = list(set(source))

for idx, line in enumerate(source):
    try:
        a, b = line.split('\t')
        if len(a) > 2:
            dest.write("{}\t{}".format(a.lower().replace('&nbsp', ''), b))
    except:
        pass
