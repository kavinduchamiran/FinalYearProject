import csv
import fasttext

def createDataset():
    # create dataset for classification
    f = open("./label_to_uri_failed.txt", "r")
    content = f.readlines()
    myMap = {}
    for x in content:
        v = x.split('\t')
        fileName = v[0][:-5]
        colId = int(v[1])+1
        label = str(v[2][:-2])
        label = ''.join(i for i in label if not i.isdigit())
        try:
            csv_f = open("../datasets/t2d_ungrouped/property/"+fileName+".csv", "r")
            reader = csv.reader(csv_f)
            # print "file open successful"
            # B = False
            for line in reader:
                if int(line[3]) == colId:
                    # print "found"
                    t=line[0],line[1],line[2],line[3]
                    sample = '__label__'+line[0]+' '+label+'\n'
                    with open('uri_failed_data.txt', 'a') as the_file:
                        the_file.write(sample)
                    # print(sample)
                    break
            # if not B: print "NOT found"
        except:
            continue

    print ('DONE: see file named uri_failed_data.txt')



# createDataset()











