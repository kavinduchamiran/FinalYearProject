ee.py
extracts all the labels in table files
get corresponding labels for subject column from instance files
get corresponding labels for other columns from lookup endpoint
write found labels to label_to_uri.txt
write not found labels (filename, col, label) to label_to_uri_failed.txt
then open label_to_uri.txt, remove duplicates, lower case -> then open label_to_uri_cleaned.txt

dbr_dbo_dbr.py / dbr_dbp_dbr.py
read label_to_uri_cleaned.txt
query dbpedia sparql for triplets where uris in label_to_uri_cleaned.txt as subjects or objects
write triplets to dbr_dbo_dbr.txt

label_dbr.txt is not used anywhere

prepare_train.py
reads dbr_dbo_dbr.txt
splits them into train test valid
create relation2id.txt, entity2id.txt