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

    dset = 'motorcycle'
    old_label = 'passendger'
    new_label = 'passenger'
    
    dset_id = dataset_model.find({'name':dset}).next()['_id']
    if category_model.find({'name':old_label}).count() > 0:
        old_label_id = category_model.find({'name':old_label}).next()['_id']
    else:
        old_label_id = -1
    if category_model.find({'name':new_label}).count() > 0:
        new_label_id = category_model.find({'name':new_label}).next()['_id']
    else:
        new_label_id = db.category_model.aggregate([{'$group':{'_id':1,'last':{'$max':'$_id'}}}]).next()['last']+1
        db.category_model.insert({'_id':new_label_id,'name':new_label,'supercategory':'','color':'#4a15bb','metadata':{},'creator':'Svetla','deleted':False,'keypoint_edges':[],'keypoint_labels':[],'keypoint_colors':[]})
        print('Created '+new_label)

    if old_label_id > 0:
        annotation_model.update_many({'dataset_id':dset_id,'category_id':old_label_id},{'$set':{'category_id':new_label_id}})
        print('Ready')
    else:
        print('Error')
    
