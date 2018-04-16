#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from application import application
from application.constants import DATASET_STORAGE_PATH
from application.utils.filters.mscocoFilter import MSCocoFilter

with application.test_request_context():
    msc = MSCocoFilter("coco/", "val2014", 0, -1)
    print msc.getAllSubCat()
    print msc.getAllSuperCat()
    # print msc.getAllSample()
