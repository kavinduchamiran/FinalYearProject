import json
import codecs
import csv

def read_t2d_table(filename):
    """
    reads a table from t2d dataset, json format
    :param filename: the path to json file
    :return: bool: table has a header row
             int: primary column index
             list of lists: column values, each column in a list
    """
    filename = './datasets/test_files/tables/' + filename
    table = json.load(codecs.open(filename,
        'r', encoding='utf-8', errors='ignore'))

    has_header = table['hasHeader']
    # todo else not 0 -> left most one with highest unique items
    key_column_idx = table['keyColumnIndex'] if table['hasKeyColumn'] else 0
    records = table['relation']

    return (has_header, key_column_idx, records)

def read_t2d_property(filename):
    """
    reads a table from t2d property file, csv format
    :param filename: the path to csv file
    :return: dict: {col_id: dbo:concept} for (some) columns in table
    """
    filename = './datasets/test_files/property/' + filename
    property = csv.reader(open(filename))
    return {int(idx): uri for uri, _, _, idx in property}

