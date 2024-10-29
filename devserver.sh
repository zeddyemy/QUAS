#!/bin/sh
source .venv/Scripts/activate
pip install -r requirements.txt
pip install --upgrade pip
python -m flask --app run:flask_app run --debug