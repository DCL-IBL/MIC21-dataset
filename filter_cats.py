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

    for d in dataset_model.find({}):
        try:
            ids = annotation_model.aggregate([{'$match':{'dataset_id':d['_id']}},{'$group':{'_id':1,'ids':{'$addToSet':'$category_id'}}}]).next()['ids']
        except:
            continue
        dataset_model.update_one({'_id':d['_id']},{'$set':{'categories':ids}})
        print(d['name'])
    quit()

    #for ct in category_model.find({}):
    #    if annotation_model.find({'category_id':ct['_id']}).count() == 0:
    #        print(ct['name']+' removed')
    #        category_model.remove({'_id':ct['_id']})
    #quit()
    
    #for d in dataset_model.find({}):
    #    if image_model.find({'dataset_id':d['_id'],'deleted':False}).count() == 0:
    #        if 'name' in d.keys():
    #            print('Remove '+d['name'])
    #        else:
    #            print('Remove '+str(d['_id']))
    #        dataset_model.remove({'_id':d['_id']})
    #quit()

    #for d in dataset_model.find({'deleted':True}):
    #    annotation_model.remove({'dataset_id':d['_id']})
    #    image_model.remove({'dataset_id':d['_id']})
    #    os.system('rm -r /home/gigov/coco-annotator'+d['directory'])
    #    print(d['name'])
    #quit()

    dset = dataset_model.find({'name':'artist'}).next()
    
    lab = ['accordeon','bbox','beam','blackboard','cannon','canvas','car windshild','car1 rear window','carving','cat 1','coach','collared shirt','contrabass','contrabass player','coxswain','crew','deer','eng-30-03710721-n','falcon','fatigues','grass ski','grass skier','guitar','hair drier','hawk','hunting dog','jean','lectern','librarian','lorry tracktor','machine gun optics','marathoner','mobile','schoolboy','schoolgirl','screen','shawl','snowboard helmet','snowboard jacket','snowboard trausers','soccer shoes','soccer sock','student','surgeon','test8','university teacher','upright','violin','wet suit','bear','snowboard boot','toaster','snowboarder','pharmacist','giraffe','dragon','carrot','elephant','hot dog','broccoli','toilet','zebra','door','pizza','sandwich','oven','fork','indian man','microwave','sink','snowboard','cat','orange','mouse','spoon','apple','window','optician','mongoloid man','old man','cow','wine glass','frisbee','sheep','cake','indian woman','old woman','knife','banana','kite','nurse','remote','mongoloid woman','scissors','white man','bed','lecturer','black woman','twin','couch','tv','white woman','mother','surgeon anesteologist','cell phone','tie','suitcase','schoolchild','potted plant','teacher','dining table']
    ids = []
    ids_str = ''
    for cname in lab:
        if len(cname) > 0:
            try:
                cat = category_model.find({'name':cname}).next()
                ids.append(cat['_id'])
                if len(ids_str) > 0:
                    ids_str = ids_str + ','
                else:
                    ids_str = '['
                ids_str = ids_str + str(cat['_id'])
            except:
                print(cname+' not found')
                #quit()
    ids_str = ids_str + ']'
    print(ids_str)

    #m = annotation_model.remove({'dataset_id':dset['_id'],'category_id':'{$not:{$in:'+ids_str+'}}'})
    m = annotation_model.remove({'category_id':'{$in:'+ids_str+'}'})
    print(m)
    m = category_model.remove({'_id':'{$in:'+ids_str+'}'})
    print(m)
    #dataset_model.update_one({'dataset_id':dset['_id']},{'$set':'{\'categories\':'+ids+'}'})
