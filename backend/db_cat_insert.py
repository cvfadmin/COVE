#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm.mapper import configure_mappers

from application import application, db
from application.constants import CATEGORY_LIST
from application.models import Base
from application.models.dataset import Dataset
from application.models.datasample import Datasample, DatasampleImage
from application.models.category import Category
from application.models.annotation import Annotation, Image_cat, BoundingBox
from application.models.relation import DatasetAnnCatAssoc, Dataset_Institution
from application.utils.dbmanage.model_insert import ModelInsert, CategoryManage 
from application.utils.dbmanage.model_query import ModelQuery
from application.utils.dbmanage.model_modify import ModelModify
from application.utils.dbmanage.coco_insert import CocoInsert
from application.utils.dbmanage.caltech_insert import CaltechInsert
from datetime import datetime

def initializeCat():
    outdoor_child =['traffic light'
                ,'fire hydrant'
		,'stop sign'
		,'parking meter'
		,'bench'
		,'coffin'
		,'fireworks'
		,'stop_sign'
		,'flashlight'
		,'gas-pump'
		,'hammock'
		,'license-plate'
		,'lightning'
		,'mailbox'
		,'picnic-table'
		,'rainbow'
		,'tombstone'
		,'waterfall'
		,'buddha'] 
    food_child = ['banana'
		,'apple'
		,'sandwich'
		,'orange'
		,'broccoli'
		,'carrot'
		,'hot dog'
		,'pizza'
		,'donut'
		,'cake'
		,'cereal-box'
		,'fried-egg'
		,'grapes'
		,'hamburger'
		,'hot-dog'
		,'ice-cream-cone'
		,'mushroom'
		,'soda-can'
		,'spaghetti'
		,'sushi'
		,'tomato'
		,'watermelon'] 
    indoor_child = ['book'
		,'clock'
		,'vase'
		,'scissors'
		,'teddy bear'
		,'hair drier'
		,'toothbrush'
		,'desk-globe'
		,'diamond-ring'
		,'dice'
		,'doorknob'
		,'eyeglasses'
		,'fire-extinguisher'
		,'bonsai'
		,'hourglass'
		,'lamp'
		,'playing-card'
		,'roulette-wheel'
		,'sextant'
		,'tambourine'
		,'yo-yo'] 
    appliance_child = ['microwave'
		,'oven'
		,'toaster'
		,'sink'
		,'refrigerator'
		,'breadmaker'
		,'lathe'
		,'self-propelled-lawn-mower'
		,'washing-machine'] 
    sports_child = ['frisbee'
		,'skis'
		,'snowboard'
		,'sports ball'
		,'kite'
		,'soccer_ball'
		,'baseball bat'
		,'baseball glove'
		,'skateboard'
		,'surfboard'
		,'tennis racket'
		,'baseball-bat'
		,'baseball-glove'
		,'basketball-hoop'
		,'billiards'
		,'bowling-ball'
		,'bowling-pin'
		,'boxing-glove'
		,'chess-board'
		,'dumb-bell'
		,'football-helmet'
		,'golf-ball'
		,'kayak'
		,'soccer-ball'
		,'tennis-ball'
		,'tennis-court'
		,'tennis-racket'
		,'treadmill'
		,'tennis-shoes'] 
    person_child = ['cartman'
		,'homer-simpson'
		,'Faces_easy'
		,'human-skeleton'
		,'Faces'
		,'jesus-christ'
		,'minotaur'
		,'people'
		,'superman'
		,'brain'
		,'faces-easy'] 
    animal_child = ['ant'
    	,'dalmatian'
    	,'platypus'
    	,'cougar_body'
    	,'brontosaurus'
    	,'pigeon'
    	,'flamingo_head'
    	,'nautilus'
    	,'cougar_face'
    	,'panda'
    	,'lobster'
    	,'wild_cat'
    	,'bird'
		,'cat'
		,'dog'
		,'horse'
		,'sheep'
		,'cow'
		,'elephant'
		,'crocodile'
		,'Leopards'
		,'stegosaurus'
		,'snoopy'
		,'okapi'
		,'hedgehog'
		,'sea_horse'
		,'flamingo'
		,'garfield'
		,'crayfish'
		,'tick'
		,'rooster'
		,'rhino'
		,'crocodile_head'
		,'beaver'
		,'bear'
		,'zebra'
		,'giraffe'
		,'bat'
		,'butterfly'
		,'camel'
		,'chimp'
		,'conch'
		,'cormorant'
		,'duck'
		,'elk'
		,'frog'
		,'gerenuk'
		,'goat'
		,'goldfish'
		,'goose'
		,'gorilla'
		,'horseshoe-crab'
		,'hummingbird'
		,'iguana'
		,'killer-whale'
		,'mussels'
		,'octopus'
		,'ostrich'
		,'owl'
		,'penguin'
		,'porcupine'
		,'raccoon'
		,'skunk'
		,'snake'
		,'spider'
		,'swan'
		,'triceratops'
		,'unicorn'
		,'hawksbill'
		,'ibis'
		,'kangaroo'
		,'greyhound'
		,'toad'
		,'crab'
		,'dolphin'
		,'leopards'
		,'llama'
		,'starfish'
		,'trilobite'] 
    vehicle_child = ['bicycle'
		,'car'
		,'motorcycle'
		,'airplane'
		,'bus'
		,'train'
		,'truck'
		,'boat'
		,'blimp'
		,'bulldozer'
		,'canoe'
		,'schooner'
		,'car_side'
		,'ferry'
		,'Motorbikes'
		,'covered-wagon'
		,'fighter-jet'
		,'fire-truck'
		,'hot-air-balloon'
		,'pram'
		,'school-bus'
		,'segway'
		,'snowmobile'
		,'speed-boat'
		,'tricycle'
		,'wheelbarrow'
		,'helicopter'
		,'ketch'] 
    furniture_child = ['chair'
		,'couch'
		,'potted plant'
		,'bed'
		,'dining table'
		,'toilet'
		,'bathtub'
		,'birdbath'
		,'hot-tub'
		,'mattress'
		,'ceiling_fan'
		,'windsor_chair'
		,'stained-glass'
		,'chandelier'
		,'menorah'] 
    accessory_child = ['backpack'
		,'umbrella'
		,'handbag'
		,'suitcase'
		,'american-flag'
		,'binoculars'
		,'coin'
		,'ladder'
		,'stapler'
		,'anchor'
		,'paperclip'
		,'pez-dispenser'
		,'saddle'
		,'screwdriver'
		,'stirrups'
		,'barrel'
		,'wheelchair'
		,'swiss-army-knife'
		,'syringe'
		,'tweezer'
		,'welding-mask'
		,'yarmulke'
		,'watch'] 
    electronic_child = ['tv'
		,'laptop'
		,'mouse'
		,'remote'
		,'keyboard'
		,'camera'
		,'cellphone'
		,'cell phone'
		,'boom-box'
		,'calculator'
		,'cd'
		,'computer-keyboard'
		,'computer-monitor'
		,'computer-mouse'
		,'floppy-disk'
		,'head-phones'
		,'ipod'
		,'joy-stick'
		,'lightbulb'
		,'megaphone'
		,'microscope'
		,'palm-pilot'
		,'paper-shredder'
		,'pci-card'
		,'photocopier'
		,'radio-telescope'
		,'rotary-phone'
		,'telephone-box'
		,'theodolite'
		,'tripod'
		,'vcr'
		,'video-projector'] 
    kitchen_child = ['bottle'
		,'wine glass'
		,'cup'
		,'fork'
		,'knife'
		,'spoon'
		,'bowl'
		,'beer-mug'
		,'chopsticks'
		,'coffee-mug'
		,'drinking-straw'
		,'frying-pan'
		,'teapot'
		,'wine-bottle'
		,'ewer'] 
    instrument_child = ['french-horn'
		,'harp'
		,'metronome'
		,'euphonium'
		,'binocular'
		,'gramophone'
		,'electric_guitar'
		,'saxophone'
		,'bass'
		,'accordion'
		,'wrench'
		,'grand_piano'
		,'tuning-fork'
		,'harpsichord'
		,'sheet-music'
		,'xylophone'
		,'guitar-pick'
		,'harmonica'
		,'mandolin'
		,'grand-piano'
		,'electric-guitar'] 
    weapon_child = ['cannon'
		,'ak47'
		,'rifle'
		,'sword'
		,'revolver'] 
    building_child = ['eiffel-tower'
		,'light-house'
		,'pyramid'
		,'minaret'
		,'skyscraper'
		,'smokestack'
		,'tower-pisa'
		,'windmill'
		,'golden-gate-bridge'
		,'teepee'] 
    plant_child = ['cactus'
		,'fern'
		,'joshua_tree'
		,'lotus'
		,'hibiscus'
		,'iris'
		,'palm-tree'
		,'clutter'
		,'sunflower'] 
    universe_child = ['comet'
		,'saturn'
		,'mars'
		,'galaxy'] 
    insects_child = ['centipede'
    	,'mayfly'
		,'cockroach'
		,'grasshopper'
		,'house-fly'
		,'praying-mantis'
		,'snail'
		,'scorpion'] 
    clothes_child = ['tie'
		,'cowboy-hat'
		,'socks'
		,'sneaker'
		,'top-hat'
		,'t-shirt'
		,'necktie'] 
    root = ModelInsert.insertCat("", None, db.session)
    image = ModelInsert.insertCat("image", root, db.session)
    outdoor = ModelInsert.insertCat("outdoor", image, db.session)
    food = ModelInsert.insertCat("food", image, db.session)
    indoor = ModelInsert.insertCat("indoor", image, db.session)
    appliance = ModelInsert.insertCat("appliance", image, db.session)
    sports = ModelInsert.insertCat("sports", image, db.session)
    person = ModelInsert.insertCat("person", image, db.session)
    animal = ModelInsert.insertCat("animal", image, db.session)
    obj = ModelInsert.insertCat("101_ObjectCategories", image, db.session)
    yin_yang = ModelInsert.insertCat("yin_yang", image, db.session)
    google = ModelInsert.insertCat("BACKGROUND_Google", image, db.session)
    vehicle = ModelInsert.insertCat("vehicle", image, db.session)
    furniture = ModelInsert.insertCat("furniture", image, db.session)
    accessory = ModelInsert.insertCat("accessory", image, db.session)
    electronic = ModelInsert.insertCat("electronic", image, db.session)
    kitchen = ModelInsert.insertCat("kitchen", image, db.session)
    instrument = ModelInsert.insertCat("instrument", image, db.session)
    weapon = ModelInsert.insertCat("weapon", image, db.session)
    building = ModelInsert.insertCat("building", image, db.session)
    plant = ModelInsert.insertCat("plant", image, db.session)
    universe = ModelInsert.insertCat("universe", image, db.session)
    insects = ModelInsert.insertCat("insects", image, db.session)
    clothes = ModelInsert.insertCat("clothes", image, db.session)
    for s in outdoor_child:
        c = ModelInsert.insertCat(s, outdoor, db.session)
        if s == "traffic light":
            ModelInsert.insertCat("traffic-light", c, db.session)
        if s == "fire hydrant":
            ModelInsert.insertCat("fire-hydrant", c, db.session)
    for s in food_child:
        c = ModelInsert.insertCat(s, food, db.session)
    for s in indoor_child:
        c = ModelInsert.insertCat(s, indoor, db.session)
        if s == "teddy bear":
            ModelInsert.insertCat("teddy-bear", c, db.session)
    for s in appliance_child:
        c = ModelInsert.insertCat(s, appliance, db.session)
    for s in sports_child:
        c = ModelInsert.insertCat(s, sports, db.session)
    for s in person_child:
        c = ModelInsert.insertCat(s, person, db.session)
    for s in animal_child:
        c = ModelInsert.insertCat(s, animal, db.session)
    for s in vehicle_child:
        c = ModelInsert.insertCat(s, vehicle, db.session)
        if s == "bicycle":
            ModelInsert.insertCat("mountain-bike", c, db.session)
            ModelInsert.insertCat("touring-bike", c, db.session)
        if s == "car":
            ModelInsert.insertCat("car-tire", c, db.session)
            ModelInsert.insertCat("steering-wheel", c, db.session)
            ModelInsert.insertCat("car-side", c, db.session)
        if s == "motorcycle":
            ModelInsert.insertCat("motorbikes", c, db.session)
        if s == "airplane":
            ModelInsert.insertCat("airplanes", c, db.session)
    for s in furniture_child:
        c = ModelInsert.insertCat(s, furniture, db.session)
    for s in accessory_child:
        c = ModelInsert.insertCat(s, accessory, db.session)
    for s in electronic_child:
        c = ModelInsert.insertCat(s, electronic, db.session)
    for s in kitchen_child:
        c = ModelInsert.insertCat(s, kitchen, db.session)
    for s in instrument_child:
        c = ModelInsert.insertCat(s, instrument, db.session)
    for s in weapon_child:
        c = ModelInsert.insertCat(s, weapon, db.session)
    for s in building_child:
        c = ModelInsert.insertCat(s, building, db.session)
    for s in plant_child:
        c = ModelInsert.insertCat(s, plant, db.session)
    for s in universe_child:
        c = ModelInsert.insertCat(s, universe, db.session)
    for s in insects_child:
        c = ModelInsert.insertCat(s, insects, db.session)
    for s in clothes_child:
        c = ModelInsert.insertCat(s, clothes, db.session)


with application.test_request_context():
    initializeCat()
    db.session.commit()
