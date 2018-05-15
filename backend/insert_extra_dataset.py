from application import app, db
from application.utils.dbmanage.model_insert import ModelInsert 
from datetime import datetime
import csv

# replace .csv file name
with app.test_request_context():
    # vegfru = db.session.query(Dataset).filter_by(name="VegFru").first()
    # if vegfru is None:
    #   vegfru = ModelInsert.insertDataset("VegFru", "https://github.com/hshustc/vegfru", "", "", False, "Saihui Hou, Yushan Feng, Zilei Wang", datetime.now(), \
    #       "", "", "", "", "VegFru: A Domain-Specific Dataset for Fine-Grained Visual Categorization", "iccv 2017", db.session)
    # ls3d_w = db.session.query(Dataset).filter_by(name="LS3D_W").first()
    # if ls3d_w is None:
    #     ls3d_w = ModelInsert.insertDataset("LS3D_W", "https://www.adrianbulat.com/face-alignment/", "", "", False, "Adrian Bulat, Georgios Tzimiropoulos", 2017, \
    #         "", "", "", "How Far Are We From Solving the 2D & 3D Face Alignment Problem? (And a Dataset of 230,000 3D Facial Landmarks)","iccv", [],\
    #         ["2D image", "3D point cloud"], ["action", "urban"], ["category", "bounding box"], [], ["Caltech"], db.session)

    # bam = db.session.query(Dataset).filter_by(name="Behance Artistic Media").first()
    # if bam is None:
    #     bam = ModelInsert.insertDataset("Behance Artistic Media", "https://bam-dataset.org/", "", "", False, "Michael J. Wilber, Chen Fang, Hailin Jin, Aaron Hertzmann, John Collomosse, Serge Belongie", 2017, 0\
    #         "", "", "", "BAM! The Behance Artistic Media Dataset for Recognition Beyond Photography", "iccv", [],\
    #         ["2D image", "video", "frames"], ["action", "object", "survellance"], ["label", "depth", "caption"], [], ["microsoft", "umich"], db.session)

    # jaad = db.session.query(Dataset).filter_by(name="Joint Attention for Autonomous Driving").first()
    # if jaad is None:
    #   jaad = ModelInsert.insertDataset("Joint Attention for Autonomous Driving", "http://data.nvision2.eecs.yorku.ca/JAAD_dataset/", "", "", False, "Amir Rasouli, Iuliia Kotseruba, John Tsotsos", 2016, \
    #       "", "", "", "", "Are They Going to Cross? A Benchmark Dataset and Baseline for Pedestrian Crosswalk Behavior", "iccv 2017", db.session)
    # db.session.commit()
    #ret = db.session.query(Dataset).join(Dataset_Topic).join(Dataset_Datatype)filter(Dataset.year == 2017).first()
    
    with open('./cove_clean_subset.csv', 'rU') as f:
        reader = csv.reader(f)
        attributes = next(reader)
        for dataset in reader:
            d = dict(zip(attributes, dataset))
            dst = ModelInsert.insertDataset(
                                d['name'], \
                                True, 
                                None, 
                                d['url'], \
                                d['thumbnail'], \
                                d['description'], \
                                "",\
                                False,\
                                d['author'],\
                                int(d['year']),\
                                d['size'],\
                                d['num_cat'],\
                                "",\
                                "",\
                                "",\
                                d['paper'], \
                                d['citations'].split(';'),\
                                d['conferences'].split(';'), \
                                d['keywords'].split(';'), \
                                d['tasks'].split(';'),\
                                d['types'].split(';'), \
                                d['topics'].split(';'), \
                                d['annotations'].split(';'), \
                                d['institutions'].split(';'),
                                db.session)
    db.session.commit()
