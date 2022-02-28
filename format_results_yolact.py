import numpy as np
import os
import json
import cv2
from pycocotools import mask

def polyFromMask(masked_arr):
    contours,_ = cv2.findContours(masked_arr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    segmentation = []
    for contour in contours:
        if contour.size >= 6:
            segmentation.append(contour.flatten().tolist())
    return segmentation

if __name__ == '__main__':
    dsets = json.load(open('current_datasets.json','r'))
    for ds in dsets:
        fname = ds['name']
        print('Working on '+fname)
        if os.path.exists(fname+'_yolact.json'):
            continue
        gt = json.load(open(fname+'_gt.json','r'))
        gt_imgs = dict()
        gt_cats = dict()
        gt_c = json.load(open('current_categories.json','r'))
        for ct in gt_c:
            gt_cats[ct['name']] = ct['id']
            #print(gt_cats)
        idir = '/datasets/'+fname

        res = json.load(open('/dir1/yolact_coco_result/yolact_'+fname+'.json','r'))
        out_json = {'images':gt['images'],'annotations':[],'categories':res['categories']}

        res_imgs = dict()
        for im in res['images']:
            res_imgs[im['id']] = im['file_name']
        res_cats = dict()
        for c in res['categories']:
            res_cats[c['id']] = c['name']
        
        for im in gt['images']:
            gt_imgs[im['file_name']] = im['id']

        for (k,ann) in enumerate(res['annotations']):
            res_id = ann['image_id']
            fn = res_imgs[res_id]
            img_id = gt_imgs[fn]
            res['annotations'][k]['image_id'] = img_id
            cid = res['annotations'][k]['category_id']
            res['annotations'][k]['category_id'] = gt_cats[res_cats[cid]]
            #res['annotations'][k]['score'] = 0.9

        out_json['annotations'] = res['annotations']
        
        fout = open(fname+'_yolact.json','w')
        fout.write(json.dumps(out_json['annotations']))
        fout.close()
