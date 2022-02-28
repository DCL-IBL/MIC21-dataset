import pymongo
import json
import shutil
import os

if __name__ == '__main__':
    client = pymongo.MongoClient('172.19.0.5',27017)
    db = client.flask
    dataset_model = db.dataset_model
    annotation_model = db.annotation_model
    image_model = db.image_model
    category_model = db.category_model
    user_model = db.user_model

    names = ['chess','skiing','weightlifting','climbing','cricket','flying','hockey','soccer','volleyball','tennis','skateboarding','swimming','rowing','roller_skating','horse_racing','steeplechase','jogging','gymnastics','golf','diving','car_racing','boxing','bowling','billiard','beach_volleyball','basketball','baseball','jumping','running','acrobatics','rhythmic gymnast']

    for n in names:
        print(n)
        dset = dataset_model.find({'name':n}).next()
        dset_id = dset['_id']
        dset_dir = dset['directory']
        
        source_folder = '/home/gigov/coco-annotator'+dset_dir
        destination_folder = '/home/jordan/comparison/'+n+'/data/'
        try:
            os.mkdir('/home/jordan/comparison/'+n)
            os.mkdir(destination_folder)
        except:
            print('exists')

        for file_name in os.listdir(source_folder):
            source = source_folder+file_name
            destination = destination_folder+file_name
            if os.path.isfile(source):
                shutil.copy(source, destination)
                print('copied', file_name)
 
 
