#!/bin/bash
BASE_DIR=$(dirname "$(readlink -f "$0")")
cd "$BASE_DIR" || echo "Can't change directory to $BASE_DIR (BASE_DIR variable)" && return
python3 -m venv env
chmod +x env/bin/activate
source env/bin/activate
pip3 install -r requirements.txt
cd "$BASE_DIR/django/api/scripts/" || echo -e "Can't change directory to $BASE_DIR/django/api/scripts/\n Check for missing directory" && return
mkdir model
wget -O model/yolov5_small_weight_gray.pt https://drive.google.com/file/d/1_zUiYfIr1EUeQ8MFLgeMGfRmbh-BcbmW/view?usp=sharing
git clone https://github.com/ultralytics/yolov5
pip3 install -r yolov5/requirements.txt
cd "$BASE_DIR" || echo -e "Can't change directory to $BASE_DIR (BASE_DIR variable)\n Something went wrong and directory was removed" && return
echo "Done. Ready to run 'python3 manage.py runserver' to start the server"