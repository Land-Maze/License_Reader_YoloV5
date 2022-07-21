BASE_DIR = $(dirname $(readlink -f $0))
cd $BASE_DIR/django/api/scripts/
git clone https://github.com/ultralytics/yolov5
pip3 install -r yolov5/requirements.txt
cd $BASE_DIR
pip3 install -r requirements.txt
echo "Done. Ready to run 'python3 manage.py runserver' to start the server"