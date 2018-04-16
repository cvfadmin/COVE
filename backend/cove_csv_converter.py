import csv

class Dataset:
    def __init__(self, name, year, author, tasks, data_types, topics, annotations, size, \
                 num_cat, description, thumbnail, url, paper, citations, conferences, institutions):
        self.name = name
        self.year = year
        self.author = author
        self.tasks = tasks
        self.data_types = data_types
        self.topics = topics
        self.annotations = annotations  
        self.size = size
        self.num_cat = num_cat
        self.description = description
        self.thumbnail = thumbnail
        self.url = url
        self.paper = paper
        self.citations = citations
        self.conferences = conferences
        self.institutions = institutions

datasets = []
# replace .csv file name
with open('./test_datasets.csv', 'r') as f:
    reader = csv.reader(f)
    attributes = next(reader)
    for dataset in reader:
        d = dict(zip(attributes, dataset))
        new_dataset = Dataset(
                            d['name'], \
                            d['year'], \
                            d['author'], \
                            d['tasks'].split(';'), \
                            d['data_types'].split(';'), \
                            d['topics'].split(';'), \
                            d['annotations'].split(';'), \
                            d['size'], \
                            d['num_cat'], \
                            d['description'], \
                            d['thumbnail'], \
                            d['url'], \
                            d['paper'], \
                            d['citations'].split(';'), \
                            d['conferences'].split(';'), \
                            d['institutions'].split(';'))

        datasets.append(new_dataset)
print len(datasets)