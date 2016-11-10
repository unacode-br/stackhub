"""
Stackhub importer.

Use this script to import the JSON data to MongoDB.

Arguments:
    -l | --load: str - required
        Accepted methods: `github`, `stackoverflow`, `learning_curve` and `trends`.
    -t | --truncate: bool - optional - default
        Delete all the documents from MongoDB collections.
    -nt | --not-truncate: bool - optional
        Do not delete the documents from MongoDB collections.

Usage:
    python importer.py -l "github stackoverflow"
        This will import data from Github and Stackoverflow and truncate all
        the documents from these collections.

    python importer.py -l trends -nt
        This will import data from Github Trends and DO NOT truncate the
        documents.
"""
import sys
import json
import argparse
from os import path
from stackhub.Stackhub import Stackhub

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--load', help='The collections aliases to import to MongoDB.', type=str, required=True)
parser.add_argument('-t', '--truncate', help='Delete all the collection documents.', dest='truncate', action='store_true', required=False)
parser.add_argument('-nt', '--not-truncate', help='Do not delete the collection documents.', dest='truncate', action='store_false', required=False)
parser.set_defaults(truncate=True)
args = parser.parse_args()

accepted = ('github', 'stackoverflow', 'learning_curve', 'lc_lang', 'trends')

_loads = str(args.load).split(' ')

loads = list(set(accepted).intersection([_l.strip() for _l in _loads]))

if len(loads) == 0:
    print('No method was accepted.')
    raise SystemExit

sh = Stackhub()

db = sh.db

collections = {
    'github': db.get_collection('github_data'),
    'stackoverflow': db.get_collection('stackoverflow_data'),
    'learning_curve': db.get_collection('learning_curve'),
    'trends': db.get_collection('github_trends'),
    'lc_lang': db.get_collection('learning_curve_all')
}

script_dir = path.dirname(path.abspath(__file__))

files = {
    'github': path.join(script_dir, 'data/github.json'),
    'stackoverflow': path.join(script_dir, 'data/stackoverflow.json'),
    'learning_curve': path.join(script_dir, 'data/learning_curve.json'),
    'trends': path.join(script_dir, 'data/trends.json'),
    'lc_lang': path.join(script_dir, 'data/lc_lang.json')
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
