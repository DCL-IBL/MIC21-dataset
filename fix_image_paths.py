import pymongo
import json
import os

if __name__ == '__main__':
    client = pymongo.MongoClient('172.19.0.2',27017)
    db = client.flask
    dataset_model = db.dataset_model
    annotation_model = db.annotation_model
    image_model = db.image_model
    category_model = db.category_model
    user_model = db.user_model

    dset_name = 'mounted police'

    dset_id = dataset_model.find({'name':dset_name}).next()['_id']
    dset_dir = dataset_model.find({'name':dset_name}).next()['directory']
    
    for img in image_model.find({'dataset_id':dset_id}):
        image_model.update_one({'_id':img['_id'],'dataset_id':dset_id},{'$set':{'path':dset_dir+img['file_name']}})
        print(img['file_name'])
    
