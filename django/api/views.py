import json
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseServerError
from django.shortcuts import render
from api.models import License
from api.apps import ApiConfig
from cv2 import VideoCapture, cvtColor, COLOR_BGR2GRAY, flip, imencode
from django.views.decorators.csrf import csrf_exempt

def gen(camera):
    while True:
        res, frame = camera.read()
        frame = cvtColor(frame, COLOR_BGR2GRAY)
        # frame = flip(frame, 3)
        frame = imencode('.jpeg', frame)[1].tobytes()
        
        if not res:
            return HttpResponseServerError()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
	# return StreamingHttpResponse(
    #                             gen(ApiConfig.web_cam),
    #                             content_type='multipart/x-mixed-replace; boundary=frame'
    #                             )
    return render(request, 'api/VideoFeed.django-html', {})


def license_plate(request):
    print(request.GET)
    model = License
    if request.method == 'GET':
        try:
            license = model.objects.get(license_number=request.GET.get('license_number'))
            return HttpResponse(json.dumps({'license_number': license.license_number, 'last_seen': license.last_seen.strftime('%Y-%m-%d %H:%M:%S')}), content_type='application/json', status=200)
        except (License.DoesNotExist):
            return HttpResponse("Not found", status=404, content_type='application/json')
        
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            model.object.create(license_number=body['license_number'])
        except (json.decoder.JSONDecodeError):
            return HttpResponse("Invalid JSON", status=400, content_type='application/json')