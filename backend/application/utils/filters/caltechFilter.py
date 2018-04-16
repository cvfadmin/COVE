#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
# from PIL import Image
from application.constants import DATASET_STORAGE_PATH, DATASET_OUTPUT_PATH
from application.models import datasample

class CaltechFilter():
    ALLOWED_EXTENSIONS = set(['png','jpeg','jpg','JPG'])    

    def __init__(self, dataDir):
        self.img_folder = os.path.join(DATASET_STORAGE_PATH, dataDir)
        self.output_folder = os.path.join(DATASET_OUTPUT_PATH, dataDir)
        self.store_path = dataDir
        self.samples = None

    def getCatList(self):
        ret = []
        for items in os.listdir(self.img_folder):
            if os.path.isfile(os.path.join(self.img_folder, items)):
                continue
            toappend = items.split(".")[-1]
            if toappend.endswith('-101'):
                toappend = toappend[0:-4]
            ret.append(toappend)
        return ret

    def getInsertList(self):
        ret = []
        for items in os.listdir(self.img_folder):
            if os.path.isfile(os.path.join(self.img_folder, items)):
                continue
            for f in os.listdir(os.path.join(self.img_folder, items)):
                file_path = os.path.join(self.img_folder, items, f)
                if os.path.isfile(file_path):
                    path = os.path.join(self.store_path,items, f)
                    format_ = f.split(".")[-1]
                    if not format_ in self.ALLOWED_EXTENSIONS:
                        continue
                    size = os.path.getsize(file_path)
                    comment = ""
                    #im = Image.open(file_path)
                    width, height = 100, 100
                    s = {}
                    s["path"] = path
                    s["width"] = width
                    s["height"] = height
                    s["format"] = format_
                    s["size"] = size
                    s["comment"] = comment
                    toappend = items.split(".")[-1]
                    if toappend.endswith('-101'):
                        toappend = toappend[0:-4]
                    s["category"] = toappend
                    ret.append(s)
        return ret

    def outputSamples(self, samples, category):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        self.samples = samples
        for s in self.samples:
            self.outputOneSample(s, category)

    def outputOneSample(self, sample, category):
        sampleout_direct = os.path.join(self.output_folder, category)
        if not os.path.exists(sampleout_direct):
            os.makedirs(sampleout_direct)
        shutil.copy2(os.path.join(DATASET_STORAGE_PATH, sample.path), os.path.join(sampleout_direct))  
        
