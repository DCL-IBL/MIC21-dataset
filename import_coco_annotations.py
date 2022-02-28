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

    f = open('new_cats','r')
    new_dsets = f.readlines()

    for d in new_dsets:
        name = d[:-1]+'_1'
        name = 'ambulance_NEW_1'
        print('Working on '+name)
        dset = dataset_model.find({'name':name}).next()
        dset_id = dset['_id']
        dset_path = dset['directory']
        cats = category_model.find()
        for c in cats:
            if annotation_model.find({'dataset_id':dset_id,'category_id':c['_id']}).count() > 0:
                dataset_model.update({'name':name},{'$addToSet':{'categories':c['_id']}})
                print('Category '+c['name']+' added')
        quit()
