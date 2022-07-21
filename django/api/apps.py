import json
from django.apps import AppConfig
from cv2 import VideoCapture
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
from api.scripts.Plate_Reader import Plate_Reader
from backend.settings import CONFIG_PATH, LOG_PLATE_READER_PATH
from os import remove
import threading

def check_frames(config, camera: VideoCapture):
    PL = Plate_Reader(config=config, camera=camera)
    while(True):
        res = PL.readImage()
            

class ApiConfig(AppConfig):
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    web_cam = VideoCapture(0)
    config = json.load(open(CONFIG_PATH, 'r'))
    
    
    def ready(self) -> None:
        self.check_frames_thread = threading.Thread(target=check_frames, args=(self.config, self.web_cam), daemon=False)
        self.check_frames_thread.start()
        return super().ready()
    