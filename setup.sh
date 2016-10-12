#!/bin/bash

pip install virtualenv
virtualenv venv

if [ ! -f ".env" ];
then
  cp .env.example .env
else
  echo "The .env file already exists."
fi
