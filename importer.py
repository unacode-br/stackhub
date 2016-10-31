"""
Stackhub importer.

Use this script to import the JSON data to MongoDB.

Arguments:
    - load: str
        Accepted methods.

Usage:
    python importer.py "github stackoverflow"
        This will import data from Github and Stackoverflow.
"""
import sys
import json
import argparse
from os import path
from stackhub.Stackhub import Stackhub

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--load', help='The collections aliases to import to MongoDB.', type=str, required=True)
parser.add_argument('-t', '--truncate', help='Delete old documents?', dest='truncate', action='store_true', required=False)
parser.add_argument('-nt', '--not-truncate', help='Delete old documents?', dest='truncate', action='store_false', required=False)
parser.set_defaults(truncate=True)
args = parser.parse_args()

accepted = ('github', 'stackoverflow', 'learning_curve', 'trends')

_loads = str(args.load).split(' ')

founds_cnt = 0
loads = []

for load in _loads:
    if load.strip() in accepted:
        founds_cnt += 1
        loads.append(load.strip())

if founds_cnt == 0:
    print('No method was accepted.')
    raise SystemExit

sh = Stackhub()

db = sh.db

collections = {
    'github': db.get_collection('github_data'),
    'stackoverflow': db.get_collection('stackoverflow_data'),
    'learning_curve': db.get_collection('learning_curve'),
    'trends': db.get_collection('github_trends')
}

script_dir = path.dirname(path.abspath(__file__))

files = {
    'github': path.join(script_dir, 'data/github.json'),
    'stackoverflow': path.join(script_dir, 'data/stackoverflow.json'),
    'learning_curve': path.join(script_dir, 'data/learning_curve.json'),
    'trends': path.join(script_dir, 'data/trends.json')
}

for method in loads:
    try:
        if args.truncate:
            deleted = collections[method].delete_many({})

            print(str(deleted.deleted_count) + ' documents deleted from ' + collections[method].name + ' collection.')

        inserted = 0

        with open(files[method], 'r') as f:
            for line in f.read().split('\n'):
                if line:
                    try:
                        lineJson = json.loads(line)
                    except (ValueError, KeyError, TypeError) as e:
                        pass
                    else:
                        collections[method].insert(lineJson)
                        inserted += 1

            f.close()

        print(str(inserted) + ' documents inserted into ' + collections[method].name + ' collection.')
    except Exception as err:
        print('Error: {0}'.format(err))
        pass
