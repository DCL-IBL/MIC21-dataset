MIC 21 Dataset
========

[MIC21 Dataset](https://dcl.bas.bg/MIC-21/dataset/) contains images from 130 thematic fields together with their ground truth annotations represented in MS COCO format. The structure of the dataset is as follows

'''
-thematic_field_name
  - data
    - image 1
    - image 2
    ...
  thematic_field_name_gt.json
'''

The data subdirectory for the respective thematic field contains the images in jpg, jpeg or png format. The *_gt.json field is a COCO format JSON file describing the polygonal object segments present in every image. Since this is a standard format, you can import the dataset in another application specific image processing of computer vision software.