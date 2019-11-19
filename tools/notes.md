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

Join all images in one big folder, maybe modifying its names (in case there are clashes)

Split in two folders, maybe 80-20, train-val

Annotate based on that, getting two different files: train.json and val.json

Check original repo for correct names. Note also that images field in json shouldn't have the full path but just the image name. Should check how this is managed by the main.py script

After that - I guess - it's just going ahead and train