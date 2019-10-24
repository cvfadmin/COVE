import json
import os

dir = os.path.dirname(os.path.abspath(__file__))

with open(dir + '/ES_docs/ES_dataset_doc.json') as json_file:
    ES_DATASET_DOC = json.load(json_file)
