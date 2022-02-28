import pymongo
import json

if __name__ == '__main__':
    client = pymongo.MongoClient('172.19.0.2',27017)
    db = client.flask
    dataset_model = db.dataset_model
    annotation_model = db.annotation_model
    image_model = db.image_model
    category_model = db.category_model
    user_model = db.user_model

    name = 'ice_skating'
    dset_id = dataset_model.find({'name':name}).next()['_id']
    f = open('statistics_for_annotations_'+name+'.txt','w')
    for ann in annotation_model.find({'dataset_id':dset_id,}):
        fn = image_model.find({'_id':ann['image_id']}).next()['file_name']
        cat = category_model.find({'_id':ann['category_id']}).next()['name']
        f.write(fn + ' ' + cat + '\n')
    f.close()
    quit()

    for dataset in dataset_model.find():
        if 'name' not in dataset.keys():
            continue
        print('Working on '+dataset['name'])
        imgs = image_model.find({'dataset_id':dataset['_id']})
        imgs_json = []
        hw = dict()
        for im in imgs:
            imgs_json.append({'id':im['_id'],
                              'width':im['width'],
                              'height':im['height'],
                              'file_name':im['file_name']})
            hw[im['_id']] = [im['width'], im['height']]
            
        anns = annotation_model.find({'dataset_id':dataset['_id']})
        anns_json = []
        for an in anns:
            #print(an['segmentation'])
            #msk = mask.frPyObjects(an['segmentation'],hw[an['image_id']][1],hw[an['image_id']][0])
            #for i in range(len(msk)):
            #    msk[i]['counts'] = msk[i]['counts'].decode('ascii')
            if an['segmentation'] == []:
                continue
            anns_json.append({'id':an['_id'],
                              'image_id':an['image_id'],
                              'category_id':int(an['category_id']),
                              'segmentation':an['segmentation'],
                              'area':an['area'],
                              'bbox':an['bbox'],
                              'iscrowd':0})

        fn = dataset['name'] + '_gt.json'
        out_json = {'images':imgs_json,'categories':cats_json,'annotations':anns_json,'info':{}}

        fout = open(fn,'w')
        fout.write(json.dumps(out_json))
        fout.close()
