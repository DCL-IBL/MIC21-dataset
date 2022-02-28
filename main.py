0;136;0cfrom detectron2.config import get_cfg
from detectron2.engine.defaults import DefaultPredictor
from detectron2.data.datasets import register_coco_instances
from detectron2.data import get_detection_dataset_dicts
from detectron2.data.detection_utils import read_image
from detectron2.data import MetadataCatalog

import numpy as np
import os
import json
import cv2
from pycocotools import mask
import argparse

def polyFromMask(masked_arr):
    contours,_ = cv2.findContours(masked_arr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    segmentation = []
    for contour in contours:
        if contour.size >= 6:
            segmentation.append(contour.flatten().tolist())
    return segmentation

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detections')
    parser.add_argument('--fname',dest='fname',type=str,help='name of the folder')
    parser.add_argument('--th',dest='th',type=float,default=0.0)
    parser.add_argument('--model',dest='model',type=int,help='number of the model')
    args = parser.parse_args()
    fname = args.fname
    
    gt = json.load(open(fname+'_gt.json','r'))
    gt_imgs = dict()
    gt_cats = dict()
    for im in gt['images']:
        #gt_imgs[os.path.basename(im['path'])] = im['id']
        gt_imgs[im['file_name']] = im['id']
    gt_c = json.load(open('categories_export.json','r'))
    for ct in gt_c:
        gt_cats[ct['name']] = ct['_id']
    print(gt_cats)
    cfg = get_cfg()

    if args.model == 1:
        cfg.merge_from_file('/home/appuser/detectron2_repo/configs/COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml')
        cfg.MODEL.WEIGHTS = 'detectron2://COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x/139653917/model_final_2d9806.pkl'
    elif args.model == 2:
        cfg.merge_from_file('/home/appuser/detectron2_repo/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_C4_1x.yaml')
        cfg.MODEL.WEIGHTS = 'detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_C4_1x/137259246/model_final_9243eb.pkl'
    elif args.model == 3:
        cfg.merge_from_file('/home/appuser/detectron2_repo/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_DC5_1x.yaml')
        cfg.MODEL.WEIGHTS = 'detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_DC5_1x/137260150/model_final_4f86c3.pkl'
    else:
        exit
        
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = args.th
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.th
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.th
    #cfg.freeze()
    pred = DefaultPredictor(cfg)
    print('predictor loaded')
    idir = '/datasets/'+fname
    out_json = {'images':[],'annotations':[],'categories':[]}
    cats = MetadataCatalog.get('coco_2017_train').thing_classes
    for ct in gt_c:
        out_json['categories'].append({'id':ct['_id'],'name':ct['name']})
    aind = 0
    for (k,f) in enumerate(os.listdir(idir)):
        if f not in gt_imgs.keys():
            continue
        img_id = gt_imgs[f]
        fn, fext = os.path.splitext(f)
        if fext != '.jpg' and fext != '.jpeg' and fext != '.png':
            continue
        img = read_image(os.path.join(idir,f))
        prediction = pred(img)
        h,w = prediction['instances'].image_size
        out_json['images'].append({'file_name':f,'height':h,'width':w,'id':img_id})
        for (ci,c) in enumerate(prediction['instances'].pred_classes):
            msk = mask.encode(np.asfortranarray(prediction['instances'].pred_masks[ci,:,:].cpu().numpy().astype(np.uint8)))
            msk['counts'] = msk['counts'].decode('ascii')
            out_json['annotations'].append({'id':aind,
                                            'category_id':gt_cats[cats[c.cpu().item()]],
                                            'image_id':img_id,
                                            #'segmentation':polyFromMask(prediction['instances'].pred_masks[ci,:,:].cpu().numpy().astype(np.uint8)),
                                            'segmentation':msk,
                                            'score':prediction['instances'].scores[ci].cpu().item()})
                                            #'iscrowd':0,
                                            #'area':np.sum(prediction['instances'].pred_masks[ci,:,:].cpu().numpy().astype(np.uint8)).astype(np.float)})
            aind = aind + 1
            if aind % 1000 == 0 :
                print(aind)
    fout = open(fname+'.json','w')
    fout.write(json.dumps(out_json['annotations']))
    fout.close()
