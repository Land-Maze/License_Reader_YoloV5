from cv2 import COLOR_BGR2GRAY, COLOR_GRAY2RGB, VideoCapture, cvtColor, COLOR_BGR2RGB
import torch 
import numpy as np
import cv2
import easyocr
import logging
from pathlib import Path
from os import mkdir
from typing import Dict, Tuple, List

class Plate_Reader(object):
    
    class Draw(object):
        
        def __init__(self, Plate_Reader) -> None:
            self._pl = Plate_Reader
        
        
            """_summary_
            Creating box with given coordinates

            Returns:
                _type_: _description_
            """
        def _plot_boxes(self, frame: cv2.Mat, result: Tuple[torch.Tensor, torch.Tensor], classes: List[str]) -> Tuple[List[str], cv2.Mat]:
            labels, cnt = result
            x_shape, y_shape = frame.shape[1], frame.shape[0]
            
            num_plates = []
            
            for i in range(len(labels)):
                row = cnt[i]
                if row[4] >= float(self._pl.CONFIDENCE_THRESHOLD):
                    x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                    cords = [x1,y1,x2,y2]

                    plate_num = self._pl.recognize_plate_easyocr(frame = frame, cords = cords, confidence_threshold = float(self._pl.EASY_OCR_THRESHOLD))

                    if(plate_num == ""):
                        continue
                    num_plates.append(plate_num)
                    frame = cvtColor(frame, COLOR_GRAY2RGB)
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    frame = cv2.rectangle(frame, (x1, y1-20), (x2, y1), (0, 255,0), -1) 
                    frame = cv2.putText(frame, f"{plate_num} - {row[4]}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255), 2)
                
            return (num_plates, frame)
        
    def __init__(self, config: dict = {}, camera = VideoCapture(0)) -> None:
        
        self._BASE_DIR = Path(__file__).parent.absolute()
        self._camera: VideoCapture = camera
        self._Draw = Plate_Reader.Draw(self)
        self._parse_config(config)
        logging.basicConfig(filename=self._BASE_DIR.parent / "logs" / "Plate_Reader.log", level=logging.INFO, format='[%(asctime)s] - %(levelname)s: %(message)s', filemode='w')
        self._EASY_OCR = easyocr.Reader(['en'])
        try:
            mkdir(self._BASE_DIR.parent / "logs")
        except FileExistsError:
            pass
        self._model = torch.hub.load(self.HUB_PATH, 'custom', source="local", path=self.MODEL_PATH, force_reload=True, verbose=False)
        
    def __str__(self) -> str:
        output = ""
        for item in self.__dict__:
            output += f"{item}: {self.__dict__[item]}\n"
            
        return output
    
    def __repr__(self) -> str:
        output = ""
        for item in self.__dict__:
            output += f"{item}-{self.__dict__[item]};"
            
        return output[:-1]
        
    def _parse_config(self, config: dict) -> None:
        
        if(not config):
            self.CONFIDENCE_THRESHOLD = 0.5
            self.MODEL_PATH = self._BASE_DIR / "models" / "yolov5_weight.pt"
            self.HUB_PATH = self._BASE_DIR / "yolov5" 
            self.EASY_OCR_THRESHOLD = 0.5
            return False
        
        for item in config:
            item: str
            setattr(self, item.upper(), config[item])
            
    def filter_text(self, region, ocr_result: str, confidence_threshold: float):
        rectangle_size = region.shape[0]*region.shape[1]
        
        plate = [] 
        for result in ocr_result:
            length = np.sum(np.subtract(result[0][1], result[0][0]))
            height = np.sum(np.subtract(result[0][2], result[0][1]))
            
            if length*height / rectangle_size > confidence_threshold:
                plate.append(result[1])
        return plate
            
    def recognize_plate_easyocr(self, frame: cv2.Mat, cords: List[int], confidence_threshold: float) -> str:
        xmin, ymin, xmax, ymax = cords    
        
        nplate = frame[int(ymin):int(ymax), int(xmin):int(xmax)]
        ocr_result = self._EASY_OCR.readtext(nplate)
        text = self.filter_text(region=nplate, ocr_result=ocr_result, confidence_threshold= confidence_threshold)

        if len(text) ==1:
            text = text[0].upper()
        return text
    
    def detectx (self, frame) -> Tuple:
        frame = [frame]
        results = self._model(frame)

        labels, cordinates = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

        return (labels, cordinates)
    
    def readImage(self) -> Tuple[cv2.Mat, List[str]]:
        res, frame = self._camera.read()
        
        if(not res):
            return (None, [])
        
        frame = cvtColor(frame, COLOR_BGR2GRAY)
        model_result = self.detectx(frame)
        plate, frame = self._Draw._plot_boxes(frame, model_result, ["license"])
        
        cv2.imwrite("frame.jpg", frame)
        return (frame, plate)