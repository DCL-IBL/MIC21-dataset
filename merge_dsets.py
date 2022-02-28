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
    
    from_dset_id = dataset_model.find({'name':from_dset}).next()['_id']
    from_dset_dir = dataset_model.find({'name':from_dset}).next()['directory']
    to_dset_id = dataset_model.find({'name':to_dset}).next()['_id']
    to_dset_dir = dataset_model.find({'name':to_dset}).next()['directory']

    for im in image_model.find({'dataset_id':from_dset_id}):
        os.rename('/home/gigov/coco-annotator'+os.path.join(from_dset_dir,im['file_name']),'/home/gigov/coco-annotator'+os.path.join(to_dset_dir,im['file_name']))
        dup_im = image_model.find({'file_name':im['file_name'],'dataset_id':to_dset_id})
        if dup_im.count() > 0:
            dup_im_ = dup_im.next()
            annotation_model.remove({'image_id':dup_im_['_id']})
            image_model.remove({'_id':dup_im_['_id']})
            print('Duplicate')
        image_model.update_one({'_id':im['_id']},{'$set':{'dataset_id':to_dset_id,'path':to_dset_dir+im['file_name']}})
        annotation_model.update_many({'dataset_id':from_dset_id,'image_id':im['_id']},{'$set':{'dataset_id':to_dset_id}})
        print(im['file_name'])
