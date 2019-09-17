import glob
import csv 
import pickle
import json
import uuid

filePathsToLabeledTables = glob.glob("./extended_instance_goldstandard/property/*.csv")  

conceptsRelatedToLiteralValues = pickle.load(open('./floatOrIntPropertyConcepts.pkl', 'rb'))

# for con in conceptsRelatedToLiteralValues:
print (len(conceptsRelatedToLiteralValues))

tblIDtoColumnsMap = {}

c = 0 
data_json = {}
remove = "$,\"[]()? -!abcdefghijklmnopqstuvw"

subject_concept = None
literal_concept = None
for pathtoProperty in filePathsToLabeledTables:
    # open property dir
    csvfile = open(pathtoProperty, 'rU')
    readCSV = csv.reader(csvfile, delimiter=',')
    # print(pathtoProperty)
    a = False
    numbers = []
    for row in readCSV:
        # if str(row[2]).strip() == :
            # subject_concept = row[0]
        if (str(row[2]) == "True"):
            subject_concept = row[0]
        if row[0] in conceptsRelatedToLiteralValues:
            # print(pathtoProperty)
            a = True
            pathToTable = pathtoProperty.replace("property", "tables").replace("csv", "json")
            # open tables dir
            # print(pathToTable)
            json_file = open(pathToTable) 
            data = json.load(json_file, encoding="cp1252")
            # print(row[0], subject_concept, int(row[3]))
            literal_concept = row[0]
            # print(data['relation'][int(row[3])])
            
            for txt in data['relation'][int(row[3])][1:]:
                for r in remove:
                    txt = txt.replace(r, '')
                if len(txt) > 0:
                    numbers.append(float(txt))
            

            
    if a:
        c += 1
        print(literal_concept, subject_concept)
        entry = {
            "uri": literal_concept,
            "literals": numbers,
            "domain": subject_concept
        }

        data_json[str(uuid.uuid4())] = entry
                           

print(c)

# with open('new_test_data.json', 'w') as outfile:
#     json.dump(data_json, outfile, indent=4 )


# for key in tblIDtoColumnsMap.keys():
#     print (key, tblIDtoColumnsMap[key])

