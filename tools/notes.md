# TFG UC3M

`lisa_transformer_original` is the original converter, before knowing that images should be in test/training folders.

`show_cropped_image.py` is just a simple script to show a cropped image based in some coordinates.

`COCO_Image_Viewer.ipynb` is a Jupyter notebook used for showing the annotations in COCO format (and so, checking that those annotations are correct)


--------------------------

# Some notes

```
>>> import pandas as pd
>>> df = pd.read_csv('total.csv')
>>> df.columns
Index(['Filename', 'Annotation tag', 'Upper left corner X',
       'Upper left corner Y', 'Lower right corner X', 'Lower right corner Y',
       'Origin file', 'Origin frame number', 'Origin track',
       'Origin track frame number'],
      dtype='object')
>>> import numpy as np
>>> df['X'] = np.where(df['Lower right corner X'] > df['Upper left corner X'], True, False)
>>> df['Y'] = np.where(df['Upper left corner Y'] > df['Lower right corner Y'], True, False)
>>> df['X'].unique()
array([ True])
>>> df['Y'].unique()
array([False])
```

So for some reason, the Ys are turned the other way around LOL - looks like this is because of the coordinate system, starting from the upper left corner, that's it.

----

Looks like the SSD repo expects everything to be in three folders: train2017, val2017 and annotations_whatever. So I need to reestructure the whole Lisa Dataset to follow that guidelines.

"images": [{"license": 3,"file_name": "000000391895.jpg","coco_url": "http://images.cocodataset.org/train2017/000000391895.jpg","height": 360,"width": 640,"date_captured": "2013-11-14 11:18:45","flickr_url": "http://farm9.staticflickr.com/8186/8119368305_4e622c8349_z.jpg","id": 391895},{"license": 4,"file_name": "000000522418.jpg","coco_url": "http://images.cocodataset.org/train2017/000000522418.jpg","height": 480,"width": 640,"date_captured": "2013-11-14 11:38:44","flickr_url": "http://farm1.staticflickr.com/1/127244861_ab0c0381e7_z.jpg","id": 522418},{"license": 3,"file_name": "000000184613.jpg","coco_url": "http://images.cocodataset.org/train2017/000000184613.jpg","height": 336,"width": 500,"date_captured": "2013-11-14 12:36:29","flickr_url": "http://farm3.staticflickr.com/2169/2118578392_1193aa04a0_z.jpg","id": 184613}

Join all images in one big folder, maybe modifying its names (in case there are clashes)

Split in two folders, maybe 80-20, train-val

Annotate based on that, getting two different files: train.json and val.json

Check original repo for correct names. Note also that images field in json shouldn't have the full path but just the image name. Should check how this is managed by the main.py script

After that - I guess - it's just going ahead and train

----

Also, the original COCO tags are not in this dataset

    # Original COCO categories
    tags = ['person','bicycle','car','motorcycle','airplane','bus','train',
        'truck','boat','traffic light','fire hydrant','stop sign','parking meter','bench',
        'bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe',
        'backpack','umbrella','handbag','tie','suitcase','frisbee','skis','snowboard',
        'sports ball','kite','baseball bat','baseball glove','skateboard','surfboard',
        'tennis racket','bottle','wine glass','cup','fork','knife','spoon','bowl','banana',
        'apple','sandwich','orange','broccoli','carrot','hot dog','pizza','donut','cake',
        'chair','couch','potted plant','bed','dining table','toilet','tv','laptop','mouse',
        'remote','keyboard','cell phone','microwave','oven','toaster','sink','refrigerator',
        'book','clock','vase','scissors','teddy bear','hair drier','toothbrush']

-----

Steps 

sudo pip install kaggle
mkdir .kaggle
touch kaggle.json
{"username":"ruromgar","key":"505bcd15331d7193d162bb7ce9c3f5af"}
kaggle datasets download mbornoe/lisa-traffic-light-dataset
unzip lisa-traffic-light-dataset.zip -d data/


----

SSD

cd SSD
#docker build . -t nvidia_ssd
nvidia-docker run --rm -it --ulimit memlock=-1 --ulimit stack=67108864 -v $COCO_DIR:/coco --ipc=host nvidia_ssd
python ./main.py --backbone resnet50 --warmup 300 --bs 4 --amp --epochs 30 --data COCO_DIR/ --save

tengo los containers; run sudo docker ps a ver si siguen ahí. El que me interesa es romantic einstein.

Ahí dentro está todo y tengo que ver qué es lo que pasa y por qué no tira (aunque tengo los modelos guardados que es lo que importa, en SSD/models)

Revisar rapidito y pista.

Problemas encontrados: docker llenaba el disco, solucionado con docker system prune --all --volumes --force

img = load_image('../COCO_DIR/val2017/daySequence1--00060.jpg')
plt.imshow(img)

from apex.fp16_utils import network_to_half

ssd300 = build_predictor('../models/models/epoch_20.pt')
ssd300 = ssd300.cuda()
ssd300 = network_to_half(ssd300.cuda())
ssd300 = ssd300.eval()

# change confidence to 0.1

json_file = '../COCO_DIR/annotations/instances_val2017.json'
with open(json_file,'r') as COCO:
    js = json.loads(COCO.read())
class_names = [ category['name'] for category in js['categories'] ]
print(class_names)

fig,ax = plt.subplots(1)
ax.imshow(out)

preds = best
if best.ndim == 0:
    preds = []
    preds.append(best.tolist())
print(preds)

for idx in preds:
    left, top, right, bottom = bboxes[idx]
    x, y, w, h = [val*300 for val in [left, top, right-left, bottom-top]]
    rect = patches.Rectangle((x, y),w,h,linewidth=1,edgecolor='r',facecolor='none')
    ax.add_patch(rect)
    ax.text(x, y, class_names[classes[idx]-1], bbox=dict(facecolor='white', alpha=0.5))
plt.show()


---------------

evaluation 

 python ./main.py --backbone resnet50 --mode evaluation --checkpoint ./models/models/epoch_20.pt --data ./COCO_DIR/

 la evaluación falla porque las anotaciones fallan. la solución es meter un par de anotaciones incorrectas

Python 3.5.3 (default, Sep 27 2018, 17:25:39) 
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pandas as pd
>>> train = pd.read_csv('training_data.csv')
>>> test = pd.read_csv('test_data.csv')
>>> train["Annotation tag"].unique()
array(['go', 'stop', 'stopLeft', 'goLeft', 'warningLeft', 'warning',
       'goForward'], dtype=object)
>>> test["Annotation tag"].unique()
array(['stop', 'go', 'warning', 'warningLeft', 'stopLeft'], dtype=object)
>>> 

solución temporal: añadirlas a mano

test["Annotation tag"][0] = "goLeft"
test["Annotation tag"][1] = "goForward"

MAZO DE IMPORTANTE HAY UN FALLO HAY UN FALLO HAY UN FALLO

LAS CATEGORIES TIENEN QUE SALIR DEL GLOBAL, PORQUE TIENEN QUE COMPARTIR ID!!!!

NO PUEDE SER STOP = 1 EN TRAINING Y STOP = 2 EN VAL!!!!

############################## INFERENCE

SSD: Siguiendo el tutorial de inferencia

Retinanet: 