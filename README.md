MIC 21 Dataset
========

[MIC21 Dataset](https://dcl.bas.bg/MIC-21/dataset/) contains images from 130 thematic fields together with their ground truth annotations represented in MS COCO format. The structure of the dataset is as follows

```
-thematic_field_name
  - data
    - image_1.jpg
    - image_2.png
    ...
  thematic_field_name_gt.json
```

The data subdirectory for the respective thematic field contains the images in jpg, jpeg or png format. The *_gt.json field is a COCO format JSON file describing the polygonal object segments present in every image. Since this is a standard format, you can import the dataset in another application specific image processing of computer vision software.

**Dataset processing scripts**

The repository contains also some utility scripts which can help to interact withe datasets when it is imported in mongodb environment such as [coco-annotator](https://github.com/jsbroks/coco-annotator).

add_new_cat_labels.py - insert for the newly added datasets
annotated_by_categories.py
links_to_images.py
annotations_by_folder.py
list_of_images.py
check_cat_consistency.py
compare_coco.py
merge_dsets.py
move_category_between_dsets.py
move_image_between_dsets.py
extract_label_from_json.py
prepare_dataset.py
filter_cats.py
prepare_ground_truth.py
filter_deleted_images.py
replace_new_cat_labels.py
fix_image_paths.py
scan_database.py
update_labels.py