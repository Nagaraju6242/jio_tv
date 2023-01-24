import requests
from django.http import HttpResponse
from .token import *
import os
import re
from django.shortcuts import render


def home(request):
    return render(request, "index.html")

def play(request):
    name = request.GET.get("c")
    return render(request, "play.html", {"c": name})


def auto_m3u_gen(request):
    response = HttpResponse(content_type='application/vnd.apple.mpegurl')
    response.write("#EXTM3U\n")
    response.write("#EXT-X-VERSION:3\n")
    response.write("#EXT-X-STREAM-INF:PROGRAM-ID=1,CLOSED-CAPTIONS=NONE,BANDWIDTH=250000,RESOLUTION=426x240\n")
    response.write("/live?c={}&q=250&e=.m3u8\n".format(request.GET.get('c')))
    response.write("#EXT-X-STREAM-INF:PROGRAM-ID=1,CLOSED-CAPTIONS=NONE,BANDWIDTH=400000,RESOLUTION=640x360\n")
    response.write("/live?c={}&q=400&e=.m3u8\n".format(request.GET.get('c')))
    response.write("#EXT-X-STREAM-INF:PROGRAM-ID=1,CLOSED-CAPTIONS=NONE,BANDWIDTH=600000,RESOLUTION=842x480\n")
    response.write("/live?c={}&q=600&e=.m3u8\n".format(request.GET.get('c')))
    response.write("#EXT-X-STREAM-INF:PROGRAM-ID=1,CLOSED-CAPTIONS=NONE,BANDWIDTH=800000,RESOLUTION=1024x576\n")
    response.write("/live?c={}&q=800&e=.m3u8\n".format(request.GET.get('c')))
    response.write("#EXT-X-STREAM-INF:PROGRAM-ID=1,CLOSED-CAPTIONS=NONE,BANDWIDTH=1200000,RESOLUTION=1280x720\n")
    response.write("/live?c={}&q=1200&e=.m3u8\n".format(request.GET.get('c')))

    return response

def live(request):
    res = HttpResponse("Not Found", status=404)
    if token != "" and request.GET.get("c") != "":
        opts = {
            "headers": {
                "User-Agent": "plaYtv/6.0.9 (Linux; Android 5.1.1) ExoPlayerLib/2.13.2"
            }
        }
        cx = requests.get("https://jiotv.live.cdn.jio.com/" + request.GET.get("c") + "/" + request.GET.get("c") + "_" + request.GET.get("q") + ".m3u8" + token, headers=opts["headers"])
        hs = cx.text
        hs = re.sub(fr'({request.GET.get("c")}_{request.GET.get("q")}-\d+\.ts)', fr'/stream?ts={request.GET.get("c")}/\1', hs)
        # hs = re.sub(request.GET.get("c") + "_" + request.GET.get("q") + "-(\d+)\.key/", '/stream?key=' + request.GET.get("c") + '/' + request.GET.get("c") + '_' + request.GET.get("q") + '-\1key', hs)
        # hs = re.sub(request.GET.get("c") + "_" + request.GET.get("q") + "-(\d+)\.ts/", '/stream?ts=' + request.GET.get("c") + '/' + request.GET.get("c") + '_' + request.GET.get("q") + '-\1ts', hs)
        hs = hs.replace("https://tv.media.jio.com/streams_live/" + request.GET.get("c") + "/", "/stream/?key=" + request.GET.get("c") + "/")
        headers = {
            "Content-Type": "application/vnd.apple.mpegurl",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Expose-Headers": "Content-Length,Content-Range",
            "Access-Control-Allow-Headers": "Range",
            "Accept-Ranges": "bytes"
        }
        res = HttpResponse(hs, headers=headers)
    return res

def stream(request):
    crm = creds['sessionAttributes']['user']['subscriberId']
    uniqueId = creds['sessionAttributes']['user']['unique']

    if request.GET.get("key"):
        headers = {
            'appkey': 'NzNiMDhlYzQyNjJm',
            'channelid': '0',
            'crmid': crm,
            'deviceId': '3022048329094879',
            'devicetype': 'phone',
            'isott': 'true',
            'languageId': '6',
            'lbcookie': '1',
            'os': 'android',
            'osVersion': '5.1.1',
            'srno': '200206173037',
            'ssotoken': ssoToken,
            'subscriberId': crm,
            'uniqueId': uniqueId,
            'User-Agent': 'plaYtv/6.0.9 (Linux; Android 5.1.1) ExoPlayerLib/2.13.2',
            'usergroup': 'tvYR7NSNn7rymo3F',
            'versionCode': '260'
        }

        cache = request.GET.get("key").replace("/", "_")

        if not os.path.isfile(cache):
            response = requests.get("https://tv.media.jio.com/streams_live/" + request.GET.get("key") + token, headers=headers)
            haystack = response.content
        else:
            with open(cache, "r") as f:
                haystack = f.read()

        return HttpResponse(haystack, content_type='application/octet-stream')

    if request.GET.get("ts"):
        response = HttpResponse(content_type='video/mp2t')
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Expose-Headers'] = 'Content-Length,Content-Range'
        response['Access-Control-Allow-Headers'] = 'Range'
        response['Accept-Ranges'] = 'bytes'
        opts = {
            "headers": {
                'User-Agent': 'plaYtv/6.0.9 (Linux; Android 5.1.1) ExoPlayerLib/2.13.2'
            }
        }
        
        res = requests.get("https://jiotv.live.cdn.jio.com/" + request.GET.get("ts"), headers=opts["headers"])
        print(res.status_code)
        response.write(res.content)
        return response
