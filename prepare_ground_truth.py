import pymongo
import json
import os
from pycocotools import mask

client = pymongo.MongoClient('172.19.0.2',27017)
db = client.flask
dataset_model = db.dataset_model
annotation_model = db.annotation_model
image_model = db.image_model
category_model = db.category_model
user_model = db.user_model

categ = []
for d in dataset_model.find({}):
    categ.append(d['name'])
out_dir1 = '/home/jordan/app1/server/uploads/'
out_dir = '/home/jordan/comparison/'

print(categ)

for cname in categ:
    print('Working on '+cname)
    cname = cname.replace(' ','_')
    os.system('cp -r /home/jordan/comparison/'+cname+'/data /home/jordan/app1/server/uploads/'+cname)
    os.system('cp /home/jordan/comparison/'+cname+'/'+cname+'_gt.json '+out_dir1+cname+'_gt.json')

    '''
    dset = dataset_model.find({'name':cname}).next()
    dset_id = dset['_id']
    dset_dir = dset['directory']
    out_json = {'images':[],'categories':[],'annotations':[],'info':{}}
    cname = cname.replace(' ','_')
    if not os.path.exists('/home/jordan/comparison/'+cname):
        os.system('mkdir /home/jordan/comparison/'+cname)
        os.system('mkdir /home/jordan/comparison/'+cname+'/data')
    try:
        os.system('rm /home/jordan/comparison/'+cname+'/data/*.*')
    except:
        print('New directory')
    os.system('cp /home/gigov/coco-annotator'+dset_dir+'/*.* /home/jordan/comparison/'+cname+'/data/')

    hw = dict()
    for im in image_model.find({'dataset_id':dset_id}):
        out_json['images'].append({'id':im['_id'],
                                  'width':im['width'],
                                  'height':im['height'],
                                   'file_name':im['file_name'],
                                   'metadata':im['metadata']})
        hw[im['_id']] = [im['width'], im['height']]

    cats_list = []
        
    anns = annotation_model.find({'dataset_id':dset_id})
    for (k,an) in enumerate(anns):
        #print(an['segmentation'])
        if an['segmentation'] == [] or (an['image_id'] not in hw.keys()):
            continue
        if int(an['category_id']) not in cats_list:
            if annotation_model.find({'dataset_id':dset_id,'category_id':int(an['category_id'])}).count() > 50:
                cats_list.append(int(an['category_id']))
        #msk = mask.frPyObjects(an['segmentation'],hw[an['image_id']][1],hw[an['image_id']][0])
        #for i in range(len(msk)):
        #    msk[i]['counts'] = msk[i]['counts'].decode('ascii')
        if int(an['category_id']) not in cats_list:
            continue
        out_json['annotations'].append({'id':k,
                                        'image_id':an['image_id'],
                                        'category_id':int(an['category_id']),
                                        'segmentation':an['segmentation'],
                                        #'segmentation':msk,
                                        'area':an['area'],
                                        'bbox':an['bbox'],
                                        'iscrowd':0,
                                        'metadata':an['metadata']})

    for ct in category_model.find({}):
        if int(ct['_id']) in cats_list:
            out_json['categories'].append({'id':int(ct['_id']),
                                           'name':ct['name'],
                                           'metadata':ct['metadata']})
            
    fout = open(out_dir+cname+'/'+cname+'_gt.json','w')
    #fout = open(out_dir+cname+'_gt.json','w')
    fout.write(json.dumps(out_json))
    fout.close()
    #os.system('cp /home/jordan/comparison/'+cname+'/'+cname+'_gt.json /home/jordan/comparison/'+cname+'/'+cname+'_train.json')
    '''
