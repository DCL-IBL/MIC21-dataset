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

    from_dset = 'astronaut'
    to_dset = 'spaceship'
    cat_names = ['space shuttle']
    no_cat_names = []

    from_dset_id = dataset_model.find({'name':from_dset}).next()['_id']
    from_dset_dir = dataset_model.find({'name':from_dset}).next()['directory']
    to_dset_id = dataset_model.find({'name':to_dset}).next()['_id']
    to_dset_dir = dataset_model.find({'name':to_dset}).next()['directory']

    try:
        no_cat_ids = category_model.aggregate([{'$match':{'name':{'$in':no_cat_names}}},{'$group':{'_id':1,'ids':{'$addToSet':'$_id'}}}]).next()['ids']
        if len(no_cat_ids) != len(no_cat_names):
            print('Check no cat names')
    except:
        no_cat_ids = []
    
    for cat_name in cat_names:
        cat_id = category_model.find({'name':cat_name}).next()['_id']
        for im in image_model.find({'dataset_id':from_dset_id}):
            anns = annotation_model.find({'dataset_id':from_dset_id,'image_id':im['_id'],'category_id':cat_id})
            no_anns = annotation_model.find({'dataset_id':from_dset_id,'image_id':im['_id'],'category_id':{'$in':no_cat_ids}})
            if anns.count() > 0 and no_anns.count() == 0:
                try:
                    os.rename('/home/gigov/coco-annotator'+from_dset_dir+im['file_name'],'/home/gigov/coco-annotator'+to_dset_dir+im['file_name'])
                    image_model.update_one({'_id':im['_id']},{'$set':{'dataset_id':to_dset_id,'path':to_dset_dir+im['file_name']}})
                    annotation_model.update_many({'dataset_id':from_dset_id,'image_id':im['_id']},{'$set':{'dataset_id':to_dset_id}})
                    print(im['file_name'])
                except:
                    print('error')
    
