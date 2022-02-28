import pymongo
import json
import os

if __name__ == '__main__':
    client = pymongo.MongoClient('172.19.0.5',27017)
    db = client.flask
    dataset_model = db.dataset_model
    annotation_model = db.annotation_model
    image_model = db.image_model
    category_model = db.category_model
    user_model = db.user_model

    dset_name = 'flying'
    dset = dataset_model.find({'name':dset_name}).next()
    dset_id = dset['_id']
    dset_path = dset['directory']

    for im in image_model.find({'dataset_id':dset_id}):
        fn = '/home/gigov/coco-annotator'+dset_path+im['file_name']
        if not os.path.exists(fn):
            print(im['file_name'])
            db.image_model.remove({'_id':im['_id']})

    quit()
