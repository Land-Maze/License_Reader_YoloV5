import json
from time import sleep
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseServerError
from django.shortcuts import render
from api.models import License, License_Detect
from api.apps import ApiConfig
from django.db.utils import IntegrityError
from cv2 import VideoCapture, cvtColor, COLOR_BGR2GRAY, flip, imencode
from django.views.decorators.csrf import csrf_exempt


def gen():
    while True:
        # res, frame = camera.read()
        # frame = cvtColor(frame, COLOR_BGR2GRAY)
        # frame = flip(frame, 3)
        frame = ApiConfig.frame
        sleep(1 / 60)
        
        frame = imencode('.jpeg', frame)[1].tobytes()
        
        # if not res:
        #     return HttpResponseServerError()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_frames(request):
    return StreamingHttpResponse(
                                gen(),
                                content_type='multipart/x-mixed-replace; boundary=frame'
                                )

def video_feed(request):
    return render(request, 'api/video_view.html', {"path": request.path}, content_type='text/html')

def database(request):
    
    return render(request, 'api/database.html', {"path": request.path}, content_type='text/html')

def settings(request):
    return render(request, 'api/settings.html', {"path": request.path}, content_type='text/html')

def records(request):
    
    def get_licenses() -> list:
        licenses = list(License.objects.values())
        return licenses
    
    def get_records(filter) -> list:
        records = list(License_Detect.objects.filter(filter).values())
        return records
    
    return render(request, 'api/records.html', {"path": request.path}, content_type='text/html')


def license_plate(request):
    print(request.GET)
    model = License
    if request.method == 'GET':
        try:
            if(request.GET.get('license_number') == None):
                return HttpResponse(json.dumps({"error":"Empty_Querry_String_License_Number"}), content_type='application/json')
            license = model.objects.get(license_number=request.GET.get('license_number'))
            try:
                last_seen = license.last_seen.strftime('%Y-%m-%d %H:%M:%S')
            except(AttributeError):
                last_seen = "None"
            return HttpResponse(json.dumps({'license_number': license.license_number, 'last_seen': last_seen, 'created': license.created.strftime('%Y-%m-%d %H:%M:%S')}), content_type='application/json', status=200)
        except (License.DoesNotExist):
            return HttpResponse(json.dumps({'error': "Not_Found"}), status=404, content_type='application/json')
        
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            model.objects.create(license_number=body['license_number'])
            return HttpResponse(json.dumps({'license_number': body['license_number']}), status=201, content_type='application/json')
        except (IntegrityError):
            return HttpResponse(json.dumps({'error': "Already_Exists"}), status=409, content_type='application/json')
        except (json.decoder.JSONDecodeError):
            return HttpResponse(json.dumps({"error": "Invalid JSON"}), status=400, content_type='application/json')

def license_records(request):
    
    model = License_Detect
    
    if(request.method == 'GET'):
        # print(request.GET)
        try:
            if(request.GET == None):
                all_records_list = []
                for item in model.objects.all():
                    all_records_list.append({'id': item.id, 'license_number': item.license_number.license_number, 'in_out': item.in_out, 'camera_feed_id': item.camera_feed_id, 'created': item.created.strftime('%Y-%m-%d %H:%M:%S')})
                return HttpResponse(json.dumps({all_records_list}), content_type='application/json')

            if(request.GET.get('license_number') != None):
                
                object_list = []
                
                for item in model.objects.filter(license_number=request.GET.get('license_number')).values():
                    object_list.append({
                        "license_number": item['license_number_id'],
                        "in_out": item['in_out'],
                        "camera_feed_id":item['camera_feed_id'],
                        "created": item['created'].strftime('%Y-%m-%d %H:%M:%S')})
                
                return HttpResponse(json.dumps(object_list), content_type='application/json')
            
            if(request.GET.get('camera_feed_id') != None):

                object_list = []
                
                for item in model.objects.filter(camera_feed_id=request.GET.get('camera_feed_id')).values():
                    object_list.append({
                        "license_number": item['license_number_id'],
                        "in_out": item['in_out'],
                        "camera_feed_id":item['camera_feed_id'],
                        "created": item['created'].strftime('%Y-%m-%d %H:%M:%S')})
                
                return HttpResponse(json.dumps(object_list), content_type='application/json')

                    # return HttpResponse(json.dumps({"error":"Empty_Querry_String_License_Number"}), content_type='application/json')
        except(License.DoesNotExist):
            pass
        
        except(KeyError):
            return HttpResponse(json.dumps({"error":"Not_Found"}), content_type='application/json')
        
        return HttpResponse(json.dumps({"error":"Querry_String_Wrong"}), content_type='application/json')
        
    
    if(request.method == 'POST'):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            model.objects.create(license_number=License.objects.get(license_number=body['license_number']), in_out=body['in_out'], camera_feed_id=body['camera_feed_id'])
        except (IntegrityError):
            return HttpResponse(json.dumps({'error': "Already_Exists"}), status=409, content_type='application/json')
        except (json.decoder.JSONDecodeError):
            return HttpResponse(json.dumps({"error": "Invalid JSON"}), status=400, content_type='application/json')
        except (KeyError):
            return HttpResponse(json.dumps({"error": "Invalid JSON"}), status=400, content_type='application/json')
        except(License.DoesNotExist):
            return HttpResponse(json.dumps({"error": "License_Does_Not_Exist"}), status=400, content_type='application/json')
        
        return HttpResponse(json.dumps({'license_number': body['license_number'], 'in_out': body['in_out'], 'camera_feed_id': body['camera_feed_id']}), status=201, content_type='application/json')