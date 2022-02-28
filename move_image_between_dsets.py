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

    from_dset = 'cellist'
    to_dset = 'conductor'
    img_names = ['wikimedia_Ford_pickup_truck_MPD_vehicle_Memphis_TN_2013-05-04_005.jpg','wikimedia_MPD_pickup_truck_Memphis_TN_Dec_2013_004.jpg','wikimedia_Washington_State_Park_Ranger_Chevy_Pickup.jpg','wikimedia_Yucatan_State_Police_Ford_F-series_pickup.jpg']
    img_ids = [202128,202106]

    from_dset_id = dataset_model.find({'name':from_dset}).next()['_id']
    from_dset_dir = dataset_model.find({'name':from_dset}).next()['directory']
    to_dset_id = dataset_model.find({'name':to_dset}).next()['_id']
    to_dset_dir = dataset_model.find({'name':to_dset}).next()['directory']
    
    # That is for deleting
    '''
    for img_id in img_ids:
        print('Working on '+str(img_id))
        im = image_model.find({'dataset_id':from_dset_id,'_id':img_id}).next()
        try:
            os.remove('/home/gigov/coco-annotator'+os.path.join(from_dset_dir,im['file_name']))
        except:
            print('Image not found')
        annotation_model.remove({'dataset_id':from_dset_id,'image_id':im['_id']})
        if annotation_model.find({'dataset_id':from_dset_id,'image_id':im['_id']}).count() == 0:
            print('Deleted '+im['file_name'])
            image_model.remove({'_id':im['_id']})

    quit()
    '''

    #for img_name in img_names:
    #    im = image_model.find({'file_name':img_name,'dataset_id':from_dset_id}).next()
    for img_id in img_ids:
        print('Working on '+str(img_id))
        im = image_model.find({'dataset_id':from_dset_id,'_id':img_id}).next()
        anns = annotation_model.find({'dataset_id':from_dset_id,'image_id':im['_id']})
        if anns.count() > 0:
            os.rename('/home/gigov/coco-annotator'+from_dset_dir+im['file_name'],'/home/gigov/coco-annotator'+to_dset_dir+im['file_name'])
            image_model.update_one({'_id':im['_id']},{'$set':{'dataset_id':to_dset_id,'path':to_dset_dir+im['file_name']}})
            annotation_model.update_many({'dataset_id':from_dset_id,'image_id':im['_id']},{'$set':{'dataset_id':to_dset_id}})
            print(im['file_name'])
    
