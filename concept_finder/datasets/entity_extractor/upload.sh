#!/usr/bin/env bash

python upload.py DBpedia_set2_test.txt
python upload.py DBpedia_set2_train.txt
python upload.py DBpedia_set2_valid.txt

python upload.py DBpedia_set1_test.txt
python upload.py DBpedia_set1_train.txt
python upload.py DBpedia_set1_valid.txt

