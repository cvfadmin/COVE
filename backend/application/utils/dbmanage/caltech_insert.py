#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from sets import Set
from sqlalchemy import func
from application.utils.dbmanage.model_insert import ModelInsert, CategoryManage
from application.utils.dbmanage.model_query import ModelQuery
from application.utils.filters.caltechFilter import CaltechFilter
from application.models.dataset import Dataset
from application.models.datasample import Datasample, DatasampleImage

class CaltechInsert():

    def __init__(self, dataDir, name, session):
        self.set_name = name
        self.cal = CaltechFilter(dataDir)
        self.cm = CategoryManage(session)
        self.session = session
        self.dst = None
        self.cat_ann_pair = Set()
        self.cat = {}

    def insertCategory(self):
        catlist = self.cal.getCatList()
        self.cm.addInsertList(catlist)
        self.cm.run()

    def insertDataset(self):
        with self.session.no_autoflush:
            self.dst = self.session.query(Dataset).filter_by(name=self.set_name).first()
        if self.dst is None:
            with self.session.no_autoflush:
                if self.set_name == "Caltech 256":
                    self.dst = ModelInsert.insertDataset(self.set_name, "https://authors.library.caltech.edu/7694/", \
                        "Caltech 256 is a set of 256 object categories containing a total of 30607 images. The original Caltech-101 was collected by choosing a set of object categories, downloading examples from Google Images and then manually screening out all images that did not fit the category. Caltech-256 is collected in a similar manner with several improvements: a) the number of categories is more than doubled, b) the minimum number of images in any category is increased from 31 to 80, c) artifacts due to image rotation are avoided and d) a new and larger clutter category is introduced for testing background rejection.",\
                        "", True, "Greg Griffin, Alex Holub, Pietro Perona", 2007, 0, \
                        "", "", "", "", "", ["classification"], \
                        ["image"], ["object"], ["category"], [], ["Caltech"],self.session)
                else:
                    self.dst = ModelInsert.insertDataset(self.set_name, "http://www.vision.caltech.edu/Image_Datasets/Caltech101/", \
                        "Caltech 101 is a data set of digital images created in September 2003. It is intended to facilitate Computer Vision research and techniques and is most applicable to techniques involving image recognition classification and categorization. Caltech 101 contains a total of 9,146 images, split between 101 distinct object categories (faces, watches, ants, pianos, etc.) and a background category. Provided with the images are a set of annotations describing the outlines of each image, along with a Matlab script for viewing.",\
                        "", True, "Fei-Fei Li, Marco Andreetto, Marc 'Aurelio Ranzato", 2006, 0, \
                        "", "", "", "", "", ["classification"], \
                        ["image"], ["object"], ["category"], [], ["Caltech"],self.session)

    def insertDatasample(self, info, id):
        dsi = ModelInsert.insertDatasampleImage(info["path"], info["format"], info["size"], info["comment"], \
                info["width"], info["height"], self.dst, self.session)
        # c = ModelQuery.getCategoryByName(info["category"], self.session)
        with self.session.no_autoflush:
            c = ModelQuery.getCategoryByName(info["category"], self.session)
        if c is None:
            print "Can't find the inserted category %s, skip" % info["category"]
            return
        self.cat[info["category"]] = c
        ann = ModelInsert.insertImageCat(dsi, c, self.session)
        self.cat_ann_pair.add((info["category"], "category"))

    def insertAllDatasample(self):
        samples = self.cal.getInsertList()
        count = 0
        total_len = len(samples)
        max_id = self.session.query(func.max(Datasample.id_)).scalar()
        if max_id is None:
            max_id = 0
        print max_id
        print "total to insert:", total_len
        for s in samples:
            count += 1
            sys.stdout.write("\r%f%%" % (100*float(count)/total_len))
            self.insertDatasample(s, max_id + count)
            sys.stdout.flush()
        print "\n"

    def insertAssoc(self):
        count = 0
        total_len = len(self.cat_ann_pair)
        print "total to insert:", total_len
        for s in self.cat_ann_pair:
            count += 1
            sys.stdout.write("\r%f%%" % (100*float(count)/total_len))
            ModelInsert.insertDatasetAnnCatAssoc(self.dst, self.cat[s[0]], s[1], self.session)
            sys.stdout.flush()
        print "\n"

    def insertAll(self):
        print "insert cats"
        self.insertCategory()
        print "insert dataset"
        self.insertDataset()
        print "insert all samples"
        self.insertAllDatasample()
        print "insert assoc"
        self.insertAssoc()
        print "commiting.." 
