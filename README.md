MIC21 image processing pipeline
========

[MIC21 image processing pipeline](https://dcl.bas.bg/MIC-21/dataset/) contains images from 130 thematic domains together with their ground truth annotations represented in MS COCO format. The structure of the dataset is as follows:

```
-thematic_field_name
  - data
    - image_1.jpg
    - image_2.png
    ...
  thematic_field_name_gt.json
```

The data subdirectory for the respective thematic domain contains the images in jpg, jpeg or png format. The *_gt.json_ field is a COCO format _JSON_ file describing the polygonal object segments presented in images. 
To accelerate the manual annotation, we have developed an image processing pipeline for object detection and object segmentation using pre-trained model structures aimed for the original COCO labeling domain.

**MIC21 image processing pipeline**

The repository contains  some utility scripts which can help to interact with the dataset when it is imported in mongodb environment such as [coco-annotator](https://github.com/jsbroks/coco-annotator).

add_new_cat_labels.py - insert for the newly added datasets

annotated_by_categories.py - list annotatated images by category name and store them into a file on disk

links_to_images.py - list a hyper-links to images in the database according to their thematic field

annotations_by_folder.py - list annotated images by thematic field

list_of_images.py - contains various quieries for the database giving a statistical overview for the annotated images

merge_dsets.py - merge two thematic fields into a single one

move_category_between_dsets.py - move all images having annotations from a specfic category between datasets

move_image_between_dsets.py - move one or several images from one thematic field to another, together with their associated annotations

prepare_dataset.py - resize images in a directory to match memory requirements for the target graphic card

filter_cats.py - remove images, annotations or categories from dataset based on various criteria

prepare_ground_truth.py - export all dataset images and annotations in JSON COCO format

filter_deleted_images.py - remove redundant images from the dataset marked as delated in coco-annotator

replace_new_cat_labels.py - replace labels in a thematic field according to a dictionary specified in replace_labels.json file.

fix_image_paths.py - scan image paths in the database for insconsistency and fix if necessary

update_labels.py - change the labeling of the specific images or differentiate labels between two distinct thematic folders
