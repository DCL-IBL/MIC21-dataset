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

    #name = 'trolleybus'
    #dset = dataset_model.find({'name':name}).next()
    for dset in dataset_model.find({}):
        dset_id = dset['_id']
        print('dset_id='+str(dset_id))
        if 'directory' not in dset.keys():
            continue
        dset_path = dset['directory']
    
        imgs = image_model.find({'dataset_id':dset_id,'deleted':True})
        #imgs = image_model.find({'dataset_id':dset_id})
        for im in imgs:
            print('Deleted '+im['file_name'])
            dset_id = im['dataset_id']
            try:
                os.remove('/home/gigov/coco-annotator'+os.path.join(dset_path,im['file_name']))
            except:
                print('Image not found')
            annotation_model.remove({'dataset_id':dset_id,'image_id':im['_id']})
            if annotation_model.find({'dataset_id':dset_id,'image_id':im['_id']}).count() == 0:
                print('Deleted '+im['file_name'])
                image_model.remove({'_id':im['_id']})
        #image_model.remove({'dataset_id':dset_id,'deleted':True})

        #for ann in annotation_model.find({'dataset_id':dset_id}):
        #    if image_model.find({'_id':ann['image_id'],'dataset_id':dset_id}).count() == 0:
        #        im = image_model.find({'_id':ann['image_id']}).next()['_id']
        #        print('No image '+str(ann['image_id'])+' dset'+str(im['dataset_id'])+' deleted '+str(im['deleted']))
