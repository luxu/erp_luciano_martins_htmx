#!/usr/bin/env bash

echo "Building project packages..."
python3 -m pip install --upgrade pip

echo "Building project packages..."
python3 -m pip install -q -r requirements.txt

echo "Migrating Database..."
python3 manage.py migrate --noinput
