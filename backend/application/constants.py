#!/usr/bin/env python
# -*- coding: utf-8 -*-

DATASET_DISPLAY_PATH = '../samples/' 
DATASET_STORAGE_PATH = '/Users/Sheng/Desktop/cove_local/frontend/samples/'
DATASET_OUTPUT_PATH = '/Users/Sheng/Desktop/cove_local/frontend/download/'

CATEGORY_LIST = set([u'', u'image', u'video', u'outdoor', u'food', u'indoor', u'appliance', u'sports', u'person', \
        u'animal', u'vehicle', u'furniture', u'accessory', u'electronic', u'kitchen', \
       u'toilet', u'teddy bear', u'cup', u'bicycle', u'kite', u'carrot', u'stop sign', \
       u'tennis racket', u'donut', u'snowboard', u'sandwich', u'motorcycle', u'oven', \
       u'keyboard', u'scissors', u'airplane', u'couch', u'mouse', u'fire hydrant', u'boat', \
       u'apple', u'sheep', u'horse', u'banana', u'baseball glove', u'tv', u'traffic light', \
       u'chair', u'bowl', u'microwave', u'bench', u'book', u'elephant', u'orange', u'tie', \
       u'clock', u'bird', u'knife', u'pizza', u'fork', u'hair drier', u'frisbee', u'umbrella', \
       u'bottle', u'bus', u'bear', u'vase', u'toothbrush', u'spoon', u'train', u'sink', \
       u'potted plant', u'handbag', u'cell phone', u'toaster', u'broccoli', u'refrigerator', \
       u'laptop', u'remote', u'surfboard', u'cow', u'dining table', u'hot dog', u'car', \
       u'sports ball', u'skateboard', u'dog', u'bed', u'cat', u'skis', u'giraffe', u'truck', \
       u'parking meter', u'suitcase', u'cake', u'wine glass', u'baseball bat', u'backpack', u'zebra' , u'clothes'])

ANNOTATION_LIST = set([u'boundingbox'])

DATASET_LIST = {u'mscoco':u'Microsoft Coco', u'caltech256':u'Caltech 256', u'caltech101':u'Caltech 101', u'vegfru':u'VegFru', u'ls3d':u'LS3D_W', u'bam':u'Behance Artistic Media', u'jaad':u'Joint Attention for Autonomous Driving'}

CONFERENCE_LIST = set([u'iccv 2017'])

CAT_SUB = {
      u'outdoor':u'image',
      u'food':u'image',
      u'indoor':u'image',
      u'appliance':u'image',
      u'sports':u'image',
      u'person':u'image',
      u'animal':u'image',
      u'vehicle':u'image',
      u'furniture':u'image',
      u'accessory':u'image',
      u'electronic':u'image',
      u'kitchen':u'image',
      u'instrument':u'image',
      u'weapon':u'image',
      u'building':u'image',
      u'plant':u'image',
      u'universe':u'image',
      u'insects':u'image',
      u'clothes':u'image',
      u'traffic light':u'outdoor',
      u'traffic-light':u'traffic light',
      u'fire hydrant':u'outdoor',
      u'fire-hydrant':u'fire hydrant',
      u'stop sign':u'outdoor',
      u'parking meter':u'outdoor',
      u'bench':u'outdoor',
      u'coffin':u'outdoor',
      u'fireworks':u'outdoor',
      u'flashlight':u'outdoor',
      u'gas-pump':u'outdoor',
      u'hammock':u'outdoor',
      u'license-plate':u'outdoor',
      u'lightning':u'outdoor',
      u'mailbox':u'outdoor',
      u'picnic-table':u'outdoor',
      u'rainbow':u'outdoor',
      u'tombstone':u'outdoor',
      u'waterfall':u'outdoor',
      u'buddha':u'outdoor',
      u'banana':u'food',
      u'apple':u'food',
      u'sandwich':u'food',
      u'orange':u'food',
      u'broccoli':u'food',
      u'carrot':u'food',
      u'hot dog':u'food',
      u'pizza':u'food',
      u'donut':u'food',
      u'cake':u'food',
      u'strawberry':u'food',
      u'cereal-box':u'food',
      u'fried-egg':u'food',
      u'grapes':u'food',
      u'hamburger':u'food',
      u'hot-dog':u'food',
      u'ice-cream-cone':u'food',
      u'mushroom':u'food',
      u'soda-can':u'food',
      u'spaghetti':u'food',
      u'sushi':u'food',
      u'tomato':u'food',
      u'watermelon':u'food',
      u'book':u'indoor',
      u'dollar_bill':u'indoor',
      u'clock':u'indoor',
      u'vase':u'indoor',
      u'scissors':u'indoor',
      u'lamp':u'indoor',
      u'teddy bear':u'indoor',
      u'teddy-bear':u'teddy bear',
      u'hair drier':u'indoor',
      u'toothbrush':u'indoor',
      u'desk-globe':u'indoor',
      u'diamond-ring':u'indoor',
      u'dice':u'indoor',
      u'doorknob':u'indoor',
      u'eyeglasses':u'indoor',
      u'fire-extinguisher':u'indoor',
      u'bonsai':u'indoor',
      u'hourglass':u'indoor',
      u'playing-card':u'indoor',
      u'roulette-wheel':u'indoor',
      u'sextant':u'indoor',
      u'tambourine':u'indoor',
      u'yo-yo':u'indoor',
      u'microwave':u'appliance',
      u'oven':u'appliance',
      u'toaster':u'appliance',
      u'sink':u'appliance',
      u'refrigerator':u'appliance',
      u'breadmaker':u'appliance',
      u'lathe':u'appliance',
      u'self-propelled-lawn-mower':u'appliance',
      u'washing-machine':u'appliance',
      u'frisbee':u'sports',
      u'skis':u'sports',
      u'snowboard':u'sports',
      u'sports ball':u'sports',
      u'kite':u'sports',
      u'baseball bat':u'sports',
      u'baseball glove':u'sports',
      u'skateboard':u'sports',
      u'surfboard':u'sports',
      u'tennis racket':u'sports',
      u'baseball-bat':u'sports',
      u'baseball-glove':u'sports',
      u'basketball-hoop':u'sports',
      u'billiards':u'sports',
      u'bowling-ball':u'sports',
      u'bowling-pin':u'sports',
      u'boxing-glove':u'sports',
      u'chess-board':u'sports',
      u'inline_skate':u'sports',
      u'dumb-bell':u'sports',
      u'football-helmet':u'sports',
      u'golf-ball':u'sports',
      u'kayak':u'sports',
      u'soccer-ball':u'sports',
      u'tennis-ball':u'sports',
      u'tennis-court':u'sports',
      u'tennis-racket':u'sports',
      u'treadmill':u'sports',
      u'tennis-shoes':u'sports',
      u'cartman':u'person',
      u'homer-simpson':u'person',
      u'human-skeleton':u'person',
      u'jesus-christ':u'person',
      u'minotaur':u'person',
      u'people':u'person',
      u'superman':u'person',
      u'brain':u'person',
      u'faces-easy':u'person',
      u'bird':u'animal',
      u'cat':u'animal',
      u'dog':u'animal',
      u'emu':u'animal',
      u'horse':u'animal',
      u'sheep':u'animal',
      u'cow':u'animal',
      u'elephant':u'animal',
      u'bear':u'animal',
      u'zebra':u'animal',
      u'giraffe':u'animal',
      u'bat':u'animal',
      u'butterfly':u'animal',
      u'camel':u'animal',
      u'chimp':u'animal',
      u'conch':u'animal',
      u'cormorant':u'animal',
      u'duck':u'animal',
      u'elk':u'animal',
      u'frog':u'animal',
      u'goat':u'animal',
      u'goldfish':u'animal',
      u'goose':u'animal',
      u'gerenuk':u'animal',
      u'gorilla':u'animal',
      u'horseshoe-crab':u'animal',
      u'hummingbird':u'animal',
      u'iguana':u'animal',
      u'killer-whale':u'animal',
      u'mussels':u'animal',
      u'octopus':u'animal',
      u'ostrich':u'animal',
      u'owl':u'animal',
      u'penguin':u'animal',
      u'porcupine':u'animal',
      u'raccoon':u'animal',
      u'skunk':u'animal',
      u'snake':u'animal',
      u'spider':u'animal',
      u'swan':u'animal',
      u'triceratops':u'animal',
      u'ant':u'animal',
      u'unicorn':u'animal',
      u'hawksbill':u'animal',
      u'ibis':u'animal',
      u'kangaroo':u'animal',
      u'greyhound':u'animal',
      u'toad':u'animal',
      u'crab':u'animal',
      u'dolphin':u'animal',
      u'leopards':u'animal',
      u'llama':u'animal',
      u'starfish':u'animal',
      u'trilobite':u'animal',
      u'bicycle':u'vehicle',
      u'mountain-bike':u'bicycle',
      u'touring-bike':u'bicycle',
      u'car':u'vehicle',
      u'car-tire':u'car',
      u'steering-wheel':u'car',
      u'car-side':u'car',
      u'motorcycle':u'vehicle',
      u'motorbikes':u'motorcycle',
      u'airplane':u'vehicle',
      u'airplanes':u'airplane',
      u'bus':u'vehicle',
      u'train':u'vehicle',
      u'truck':u'vehicle',
      u'boat':u'vehicle',
      u'blimp':u'vehicle',
      u'bulldozer':u'vehicle',
      u'canoe':u'vehicle',
      u'covered-wagon':u'vehicle',
      u'fighter-jet':u'vehicle',
      u'fire-truck':u'vehicle',
      u'hot-air-balloon':u'vehicle',
      u'pram':u'vehicle',
      u'school-bus':u'vehicle',
      u'segway':u'vehicle',
      u'snowmobile':u'vehicle',
      u'speed-boat':u'vehicle',
      u'tricycle':u'vehicle',
      u'wheelbarrow':u'vehicle',
      u'helicopter':u'vehicle',
      u'ketch':u'vehicle',
      u'chair':u'furniture',
      u'couch':u'furniture',
      u'potted plant':u'furniture',
      u'bed':u'furniture',
      u'dining table':u'furniture',
      u'toilet':u'furniture',
      u'bathtub':u'furniture',
      u'birdbath':u'furniture',
      u'hot-tub':u'furniture',
      u'mattress':u'furniture',
      u'stained-glass':u'furniture',
      u'chandelier':u'furniture',
      u'menorah':u'furniture',
      u'backpack':u'accessory',
      u'umbrella':u'accessory',
      u'handbag':u'accessory',
      u'suitcase':u'accessory',
      u'american-flag':u'accessory',
      u'binoculars':u'accessory',
      u'coin':u'accessory',
      u'ladder':u'accessory',
      u'paperclip':u'accessory',
      u'pez-dispenser':u'accessory',
      u'saddle':u'accessory',
      u'screwdriver':u'accessory',
      u'stirrups':u'accessory',
      u'swiss-army-knife':u'accessory',
      u'syringe':u'accessory',
      u'tweezer':u'accessory',
      u'welding-mask':u'accessory',
      u'yarmulke':u'accessory',
      u'watch':u'accessory',
      u'tv':u'electronic',
      u'laptop':u'electronic',
      u'mouse':u'electronic',
      u'remote':u'electronic',
      u'keyboard':u'electronic',
      u'cell phone':u'electronic',
      u'boom-box':u'electronic',
      u'calculator':u'electronic',
      u'cd':u'electronic',
      u'computer-keyboard':u'electronic',
      u'computer-monitor':u'electronic',
      u'computer-mouse':u'electronic',
      u'floppy-disk':u'electronic',
      u'head-phones':u'electronic',
      u'headphone':u'electronic',
      u'ipod':u'electronic',
      u'joy-stick':u'electronic',
      u'lightbulb':u'electronic',
      u'megaphone':u'electronic',
      u'microscope':u'electronic',
      u'palm-pilot':u'electronic',
      u'paper-shredder':u'electronic',
      u'pci-card':u'electronic',
      u'photocopier':u'electronic',
      u'radio-telescope':u'electronic',
      u'rotary-phone':u'electronic',
      u'telephone-box':u'electronic',
      u'theodolite':u'electronic',
      u'tripod':u'electronic',
      u'vcr':u'electronic',
      u'video-projector':u'electronic',
      u'bottle':u'kitchen',
      u'wine glass':u'kitchen',
      u'cup':u'kitchen',
      u'fork':u'kitchen',
      u'knife':u'kitchen',
      u'spoon':u'kitchen',
      u'bowl':u'kitchen',
      u'beer-mug':u'kitchen',
      u'chopsticks':u'kitchen',
      u'coffee-mug':u'kitchen',
      u'drinking-straw':u'kitchen',
      u'frying-pan':u'kitchen',
      u'teapot':u'kitchen',
      u'wine-bottle':u'kitchen',
      u'ewer':u'kitchen',
      u'french-horn':u'instrument',
      u'harp':u'instrument',
      u'tuning-fork':u'instrument',
      u'harpsichord':u'instrument',
      u'sheet-music':u'instrument',
      u'xylophone':u'instrument',
      u'guitar-pick':u'instrument',
      u'harmonica':u'instrument',
      u'mandolin':u'instrument',
      u'grand-piano':u'instrument',
      u'electric-guitar':u'instrument',
      u'cannon':u'weapon',
      u'ak47':u'weapon',
      u'rifle':u'weapon',
      u'sword':u'weapon',
      u'revolver':u'weapon',
      u'eiffel-tower':u'building',
      u'light-house':u'building',
      u'pyramid':u'building',
      u'pagoda':u'building',
      u'minaret':u'building',
      u'skyscraper':u'building',
      u'smokestack':u'building',
      u'tower-pisa':u'building',
      u'windmill':u'building',
      u'golden-gate-bridge':u'building',
      u'teepee':u'building',
      u'cactus':u'plant',
      u'water_lilly':u'plant',
      u'fern':u'plant',
      u'hibiscus':u'plant',
      u'iris':u'plant',
      u'palm-tree':u'plant',
      u'clutter':u'plant',
      u'sunflower':u'plant',
      u'comet':u'universe',
      u'saturn':u'universe',
      u'mars':u'universe',
      u'galaxy':u'universe',
      u'centipede':u'insects',
      u'dragonfly':u'insects',
      u'cockroach':u'insects',
      u'grasshopper':u'insects',
      u'house-fly':u'insects',
      u'praying-mantis':u'insects',
      u'snail':u'insects',
      u'scorpion':u'insects',
      u'tie':u'clothes',
      u'cowboy-hat':u'clothes',
      u'socks':u'clothes',
      u'sneaker':u'clothes',
      u'top-hat':u'clothes',
      u't-shirt':u'clothes',
      u'necktie':u'clothes'
}