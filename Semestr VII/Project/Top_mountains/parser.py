import json
import os


def get_paths():
    paths = []

    walk_dir = '.'

    for root, subdirs, files in os.walk(walk_dir):
        list_file_path = os.path.join(root, 'my-directory-list.txt')

        with open(list_file_path, 'wb') as list_file:
            for filename in files:
                file_path = os.path.join(root, filename)
                if file_path.split('.')[-1] == 'geojson':
                    paths.append(file_path)
    return paths


def open_file(path):
    with open(path) as f:
        gj = json.loads(f.read())

    return gj

def get_database():
    paths = get_paths()
    db = []
    for path in paths:
        try:
            f = open_file(path)
            db.append(f)
        except:
            pass
    return db

db = get_database()

coordinates = {}
for record in db:
    coord = record['geometry']['coordinates']
    if coord[0] is not None and coord[1] is not None:
        coordinates[record['properties']['name']]=[coord,record['properties']['meters']]

coordinates
