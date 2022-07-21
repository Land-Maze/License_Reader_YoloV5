#!/bin/bash
BASE_DIR=$(dirname $(readlink -f $0))
pip3 install venv
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt
cd $BASE_DIR/django/api/scripts/
mkdir model
wget -O model/yolov5_small_weight_gray.pt https://drive.google.com/file/d/1_zUiYfIr1EUeQ8MFLgeMGfRmbh-BcbmW/view?usp=sharing
git clone https://github.com/ultralytics/yolov5
pip3 install -r yolov5/requirements.txt
cd $BASE_DIR
echo "Done. Ready to run 'python3 manage.py runserver' to start the server"