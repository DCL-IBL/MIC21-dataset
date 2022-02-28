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

    f = open('replace_cats','r')
    dsets = f.readlines()
    f.close()
    f = open('label_replacement_table.json','r')
    reptab = json.loads(f.read())
    f.close()

    max_cat_id = (int)(category_model.aggregate([{"$group":{"_id":1,"mi":{"$max":"$_id"}}}]).next()['mi'])
    
    for d in dsets:
        dname = d[:-1]
        dset_id = dataset_model.find({'name':dname}).next()['_id']
        print('Working on '+dname)
        if dname not in reptab.keys():
            continue
        rep = reptab[dname]
        print(rep)
        for orig in rep.keys():
            newc = rep[orig]
            if category_model.find({'name':newc}).count() == 0:
                print('New category '+newc)
                max_cat_id = max_cat_id + 1
                category_model.insert({"_id":max_cat_id,
                                       "name":newc,
                                       "supercategory":"",
                                       "color":"#5fe639",
                                       "metadata":{},
                                       "creator":"dcl2",
                                       "deleted":"false",
                                       "keypoint_edges" : [ ],
                                       "keypoint_labels" : [ ],
                                       "keypoint_colors" : [ ]})
            new_id = (int)(category_model.find({'name':newc}).next()['_id'])
            old_id = (int)(category_model.find({'name':orig}).next()['_id'])
            annotation_model.update_many({'dataset_id':dset_id,'category_id':old_id},{"$set":{'category_id':new_id}})
            dataset_model.update_one({'_id':dset_id},{"$pull":{'categories':old_id}})
            dataset_model.update_one({'_id':dset_id},{"$addToSet":{'categories':new_id}})     
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
