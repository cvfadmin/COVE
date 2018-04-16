#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from sets import Set
from sqlalchemy import func
from application.utils.dbmanage.model_insert import ModelInsert
from application.utils.filters.mscocoFilter import MSCocoFilter
from application.models.dataset import Dataset
from application.models.datasample import Datasample, DatasampleImage
from application.models.category import Category

class CocoInsert():

    def __init__(self, dataDir, dataType, mscStart, mscRange, session):
        self.msc = MSCocoFilter(dataDir, dataType, mscStart, mscRange)
        self.superCats = {}
        self.cats = {}
        self.session = session
        self.dst = None
        self.cat_ann_pair = Set()

    def insertDataset(self):
        self.dst = self.session.query(Dataset).filter_by(name="Microsoft Coco").first()
        if self.dst is None:
            self.dst = ModelInsert.insertDataset("Microsoft Coco", "http://cocodataset.org/", "COCO is a large-scale object detection, segmentation, and captioning dataset. COCO has several features: Object segmentation, Recognition in context, Superpixel stuff segmentation,330K images (>200K labeled),1.5 million object instances, 80 object categories, 91 stuff categories, 5 captions per image, 250,000 people with keypoints", "", True, "Tsung-Yi Lin, Genevieve Patterson, Matteo R. Ronchi, Yin Cui, Michael Maire, Serge Belongie, Lubomir Bourdev, Ross Girshick, James Hays, Pietro Perona, Deva Ramanan, Larry Zitnick, Piotr Dollar", 2017, 0,\
             "", "", "", "", "", ["recognition","classification","segmentation"],\
             ["image","video"], ["object"], ["boundingbox"], [], ["Microsoft"],self.session)

    def insertSuperCategory(self, imageCat):
        supercats = self.msc.getAllSuperCat()
        for sc in supercats:
            # self.superCats[sc] = self.session.query(Category).filter_by(type_name=sc).first()
            self.superCats[sc] = ModelInsert.insertCat(sc, imageCat, self.session)
    
    def insertCategory(self):
        cats = self.msc.getAllCat()
        for c in cats:
            if c["category"] != c["supercategory"]:
                # self.cats[c["category"]] = self.session.query(Category).filter_by(type_name=c["category"]).first()
                self.cats[c["category"]] = ModelInsert.insertCat(c["category"], self.superCats[c["supercategory"]], self.session)
            else:
                self.cats[c["category"]] = self.superCats[c["supercategory"]]

    def insertAllDatasample(self):
        samples = self.msc.getAllSample()
        count = 0
        max_id = self.session.query(func.max(Datasample.id_)).scalar()
        if max_id is None:
            max_id = 0
        print max_id
        total_len = len(samples)
        for s in samples:
            count += 1
            sys.stdout.write("\r%f%%" % (100*float(count)/total_len))
            self.insertDatasample(s, max_id + count)
            sys.stdout.flush()
        print "\n"

    def insertDatasample(self, info, id):
        dsi = ModelInsert.insertDatasampleImage(info["path"], info["format"], info["size"], info["comment"], \
                info["width"], info["height"], self.dst, self.session)
        for bbox in info["boundingbox"]:
            box = ModelInsert.insertBoundingBox(bbox, id, self.cats[info["category"]], self.session)
        self.cat_ann_pair.add((info["category"], "boundingbox"))

    def insertAssoc(self):
        count = 0
        total_len = len(self.cat_ann_pair)
        for s in self.cat_ann_pair:
            count += 1
            sys.stdout.write("\r%f%%" % (100*float(count)/total_len))
            ModelInsert.insertDatasetAnnCatAssoc(self.dst, self.cats[s[0]], s[1], self.session)
            sys.stdout.flush()
        print "\n"

    def insertAll(self, imageCat):
        print "insert dataset"
        self.insertDataset()
        print "insert supercats"
        self.insertSuperCategory(imageCat)
        print "insert cats"
        self.insertCategory()
        print "insert all samples"
        self.insertAllDatasample()
        print "insert assoc"
        self.insertAssoc()
        print "commiting.."
