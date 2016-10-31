#!/bin/bash

set -e

MONGO_HOST=127.17.0.1
MONGO_PORT=27017
MONGO_DATABASE=local
MONGO_USERNAME=
MONGO_PASSWORD=

PATH=$(pwd)

# Import Github data.
if [ -z "$MONGO_USERNAME" ]; then
  mongoimport -h $MONGO_HOST:$MONGO_PORT -d $MONGO_DATABASE -c github_data --file $PATH/github.json
else
  mongoimport -h $MONGO_HOST:$MONGO_PORT -d $MONGO_DATABASE -c github_data -u $MONGO_USERNAME -p $MONGO_PASSWORD --file $PATH/github.json
fi

# Import Stackoverflow data.
if [ -z "$MONGO_USERNAME" ]; then
  mongoimport -h $MONGO_HOST:$MONGO_PORT -d $MONGO_DATABASE -c stackoverflow_data --file $PATH/stackoverflow.json
else
  mongoimport -h $MONGO_HOST:$MONGO_PORT -d $MONGO_DATABASE -c stackoverflow_data -u $MONGO_USERNAME -p $MONGO_PASSWORD --file $PATH/stackoverflow.json
fi

# Import Github Trends data.
if [ -z "$MONGO_USERNAME" ]; then
  mongoimport -h $MONGO_HOST:$MONGO_PORT -d $MONGO_DATABASE -c github_trends --file $PATH/trends.json
else
  mongoimport -h $MONGO_HOST:$MONGO_PORT -d $MONGO_DATABASE -c github_trends -u $MONGO_USERNAME -p $MONGO_PASSWORD --file $PATH/trends.json
fi

# Import Learning Curve data.
if [ -z "$MONGO_USERNAME" ]; then
  mongoimport -h $MONGO_HOST:$MONGO_PORT -d $MONGO_DATABASE -c learning_curve --file $PATH/learning_curve.json
else
  mongoimport -h $MONGO_HOST:$MONGO_PORT -d $MONGO_DATABASE -c learning_curve -u $MONGO_USERNAME -p $MONGO_PASSWORD --file $PATH/learning_curve.json
fi
