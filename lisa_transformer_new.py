import pandas as pd
import json
import csv
import os
import re


def get_folders(annotations=False):
    # Getting dataset root path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lisa_path = os.path.join(dir_path, 'lisa-traffic-light-dataset')

    # Image folders names
    day_train_folders   = [os.path.join('dayTrain', f'dayClip{i}') for i in range(1, 14)]
    night_train_folders = [os.path.join('nightTrain', f'nightClip{i}') for i in range(1, 6)]
    main_folders        = ['daySequence1', 'daySequence2', 'nightSequence1', 'nightSequence2']

    folders = day_train_folders + night_train_folders + main_folders

    if annotations:
        folders = [os.path.join(lisa_path, 'Annotations', i) for i in folders]
    else:
        folders = [os.path.join(lisa_path, i) for i in folders]

    return folders


def get_full_csv():
    columns = ['Filename', 'Annotation tag', 'Upper left corner X', 'Upper left corner Y', 'Lower right corner X', 
        'Lower right corner Y', 'Origin file', 'Origin frame number', 'Origin track', 'Origin track frame number']
    df = pd.DataFrame(columns=columns)
    total = 0
    for f in get_folders(annotations=True):
        new_df = pd.read_csv(os.path.join(f, 'frameAnnotationsBOX.csv'), sep=';')
        print('Number of rows: ' + str(new_df.shape[0]))
        total += new_df.shape[0]
        df = df.merge(new_df, how='outer', left_on=columns, right_on=columns)

    df.to_csv('lisa-traffic-lights-dataset.csv', index=False)
    print('Total: ' + str(df.shape[0]))
    print('Expected total: ' + str(total))


def get_segmentation(upper_left_x, upper_left_y, lower_right_x, lower_right_y):
    # Vertices are: 
    # Upper left  -> both x y given
    # Upper right -> x is the same as lower right; y is the same as upper left
    # Lower left  -> x is the same as upper left;  y is the same as lower right
    # Lower right -> both x y given
    # Coordinates are counted from the upper left corner of the pic

    return [[
        upper_left_x, upper_left_y,
        lower_right_x, upper_left_y,
        upper_left_x, lower_right_y,
        lower_right_x, lower_right_y
    ]]


def get_area(upper_left_x, upper_left_y, lower_right_x, lower_right_y):
    # Area is width * height
    # Width is lower_right_x - upper_left_x (right X - left X)
    # Height is upper_left_y - lower_right_y (upper Y - lower Y)
    # Height is negative because of the coordinates!

    return (lower_right_x - upper_left_x)*(-(upper_left_y - lower_right_y))


def get_bbox(upper_left_x, upper_left_y, lower_right_x, lower_right_y):
    # The COCO bounding box format is [top left x position, top left y position, width, height]
    # Top left x position is upper_left_x
    # Top left y position is upper_left_y
    # Width is lower_right_x - upper_left_x (right X - left X)
    # Height is upper_left_y - lower_right_y (upper Y - lower Y)
    # Height is negative because of the coordinates!

    return [upper_left_x, upper_left_y, (lower_right_x - upper_left_x), (-(upper_left_y - lower_right_y))] 


def get_info():
    return {
        "description": "LISA Traffic Sign Dataset",
        "url": "http://cvrr.ucsd.edu/LISA/lisa-traffic-sign-dataset.html",
        "version": "2.0",
        "year": 2018
    }


def get_licenses():
    return [
        {
            "url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
            "id": 1,
            "name": "CC BY-NC-SA 4.0"
        }
    ]


def get_images():
    # Full path of each image folder
    folders = [os.path.join(i, 'frames') for i in get_folders()]

    # Defining folder id using the folder path as key for the dict
    folders_id = {folder:f'{i:02d}' for i, folder in enumerate(folders)}

    images = []
    for folder in folders:
        for f in os.listdir(folder):
            # Sanity check in case someone has put some random not-jpg-file in the folders
            if f.endswith('.jpg'):

                folder_id = f'{str(folders_id[folder])}'
                img_id    = re.search('(?<=--)(.*[^.jpg])', f).group() # Everything between the -- and the .jpg

                images.append(
                {
                    "license": 1,
                    "file_name": os.path.join(folder, f), # Full path
                    "height": 960,
                    "width": 1280,
                    "id": int(f'{folder_id}{img_id}')
                })

    return images


def get_categories():
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

    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(os.path.join(dir_path, 'total.csv'), index_col=False)

    tags.extend(df['Annotation tag'].unique().tolist())
    print('Tags len is: ' + str(len(tags)))

    categories = []
    for i, t in enumerate(tags, 1):
        categories.append(
            {"supercategory": "", "id": i, "name": t}
        )
    
    return categories


def get_annotations(images, categories):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(os.path.join(dir_path, 'total.csv'), index_col=False)

    # Converting the dataframe into a list of lists
    data = df.values.tolist()

    # Each element in data is a 11-element list with the following fields:
    # 0. Filename
    # 1. Annotation tag
    # 2. Upper left corner X
    # 3. Upper left corner Y
    # 4. Lower right corner X 
    # 5. Lower right corner Y
    # 6. Origin file
    # 7. Origin frame number
    # 8. Origin track
    # 9. Origin track frame number

    annotations = []
    total = len(data)
    for i, d in enumerate(data, 1):

        # Getting image ID from images based on filename (d[0])
        # Since filename has the format dayTrain/dayClip1--00347.jpg we need to strip from the slash
        filename = d[0].rsplit('/')[1]
        image_id = [i["id"] for i in images if i["file_name"].endswith(filename)][0]

        # Getting category ID from categories based on name (d[1])
        category_id = [c["id"] for c in categories if c["name"] == d[1]][0]

        segmentation = get_segmentation(d[2], d[3], d[4], d[5])
        area         = get_area(d[2], d[3], d[4], d[5])
        bbox         = get_bbox(d[2], d[3], d[4], d[5])

        annotations.append({
            "segmentation": segmentation, 
            "area": area,
            "iscrowd": 0,
            "image_id": image_id,
            "bbox": bbox,
            "category_id": category_id,
            "id": i 
        })
        print(f'Processed {i} of {total}')
    return annotations


def main():
    get_full_csv()

    info = get_info()
    licenses = get_licenses()
    images = get_images()
    categories = get_categories()
    annotations = get_annotations(images, categories)

    data = {
        "info": info,
        "licenses": licenses,
        "images": images,
        "annotations": annotations,
        "categories": categories
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

main()