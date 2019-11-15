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


So for some reason, the Ys are turned the other way around LOL