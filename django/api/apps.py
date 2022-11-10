import json
from django.apps import AppConfig
from cv2 import VideoCapture
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
from api.scripts.Plate_Reader import Plate_Reader
from backend.settings import CONFIG_PATH, LOG_PLATE_READER_PATH
from collections import Counter
import threading

def addPlateRecord(license_number: str, in_out: str, camera_feed_id: int, COOLDOWN_TIME: int) -> None:
    from api.models import License_Detect, License
    
    model = License_Detect
    
    try:
        license_istance = License.objects.get(license_number=license_number)
    except(License.DoesNotExist):
        print("License not found")
        return
    
    from datetime import datetime
    from time import mktime, time
    
    license_records_list = list(model.objects.filter(license_number=license_number, in_out=in_out, camera_feed_id=camera_feed_id).values())
    last_record = license_records_list[-1]
    
    last_record_time_unix = int(mktime(last_record['created'].timetuple()))
    
    if(time() - last_record_time_unix < COOLDOWN_TIME):
        print("Cooldown time not passed")
        return
    
    print("Adding record")
    model.objects.create(license_number=license_istance, in_out=in_out, camera_feed_id=camera_feed_id)
    # model.objects.update(license_number=license_istance.license_number)
    from django.utils import timezone
    import pytz
    timezone.now()
    license_istance.last_seen = datetime.now(tz=pytz.UTC)
    license_istance.save()



def check_frames(config, camera: VideoCapture, in_out: str, camera_feed_id: int):
    PL = Plate_Reader(config=config, camera=camera)
    pool = ['' for _ in range(config['POOL_SIZE'])]
    while(True):
        # print(pool)
        res = PL.readImage()
        
        try:
            plate = res[1][0]
        except(IndexError):
            plate = []
            
        frame_res = res[0]
        
        if((plate != []) & (plate != [[]])):
            pool.append(plate)
            pool.pop(0)
            
            tmp = dict(Counter(pool))
            
            if(tmp[plate] >= int(len(pool) / 2) + 1):
                pool = ['' for _ in range(10)]
                print(f"Plate: {plate}", end='\t')
                plate = plate.upper().replace(' ', '')
                print(f"Plate_Number: {plate}")
                
                addPlateRecord(plate, in_out, camera_feed_id, config['COOLDOWN_TIME'])
                
                    
            
        ApiConfig.frame = frame_res
        
        
                
            

class ApiConfig(AppConfig):
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    web_cam = VideoCapture(0)
    config = json.load(open(CONFIG_PATH, 'r'))
    frame = web_cam.read()[1] # Camera IN №1
    
    
    def ready(self) -> None:
        self.check_frames_thread = threading.Thread(target=check_frames, args=(self.config, self.web_cam, "in", 1), daemon=False)
        self.check_frames_thread.start()
        return super().ready()
    
        