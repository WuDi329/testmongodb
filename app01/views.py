from django.http import JsonResponse
from app01.models import Straceinfo
import os
import re

from django.shortcuts import render, HttpResponse

def get(request):
    instruction = 'strace -c -v -o ./strace.txt /home/wudi/tinyserver_sta/Tiny-WebServer/tiny 7000 &  ' \
                  '&& /home/wudi/Desktop/htstress/htstress  -n 10000 -c 100 -t 8 localhost:7000 >/dev/null 2>&1'
    os.system(instruction)
    with open('strace.txt', 'r') as f:
        data = f.readlines()
    print(data[2])

    e = Straceinfo.objects.create(
        elf_name='tiny_static',
        params='7000',
        msg=[
            {'name': re.findall(r'[a-zA-Z]+', data[2])[0], 'per_time': re.findall(r'\d+', data[2])[0],
             'call_times': re.findall(r'\d+', data[2])[1], 'percent': re.findall(r'\d+.\d+', data[2])[0]},
            # {'name': 'read', 'per_time': '4', 'call_times': '82194', 'percent': '28.84'},
            # {'name': 'closes', 'per_time': '5', 'call_times': '31037', 'percent': '14.15'},
            # {'name': 'openat', 'per_time': '5', 'call_times': '20619', 'percent': '8.30'},
            # {'name': 'stat', 'per_time': '5', 'call_times': '20496', 'percent': '8.10'}
        ]
    )
    e.save()
    print(data[2])
    return JsonResponse({'code': 20000, 'msg': 'add successfully'})
# Create your views here.
