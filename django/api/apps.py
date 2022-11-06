import json
from django.apps import AppConfig
from cv2 import VideoCapture
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
from api.scripts.Plate_Reader import Plate_Reader
from backend.settings import CONFIG_PATH, LOG_PLATE_READER_PATH
from os import fchmod, remove
from collections import Counter
import threading

def check_frames(config, camera: VideoCapture):
    PL = Plate_Reader(config=config, camera=camera)
    pool = ['' for _ in range(10)]
    while(True):
        print(pool)
        res = PL.readImage()
        
        plate = res[1]
        frame_res = res[0]
        
        if((plate != []) & (plate != [[]])):
            pool.append(plate)
            pool.pop(0)
            
            # tmp = dict(Counter(pool))
            
            # if(tmp[plate][0] >= 5):
            #     pool = ['' for _ in range(10)]
            #     print(f"Plate: {plate}")
            #     print(f"Pool: {pool}")
                    
            
        ApiConfig.frame = frame_res
        
        
                
            

class ApiConfig(AppConfig):
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    web_cam = VideoCapture(0)
    config = json.load(open(CONFIG_PATH, 'r'))
    frame = web_cam.read()[1]
    
    
    def ready(self) -> None:
        self.check_frames_thread = threading.Thread(target=check_frames, args=(self.config, self.web_cam), daemon=False)
        self.check_frames_thread.start()
        return super().ready()
    
        