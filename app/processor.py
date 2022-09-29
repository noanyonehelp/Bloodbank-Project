import datetime
from django.conf import settings

from .models import Visitor_Infos

import socket
import random

def save_visitor_infos(request):
    present_date = None
    try:
        #----- get visitor ip -----#
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')    
        #----- check if ip adress is valid -----#
        try:
            socket.inet_aton(ip)
            ip_valid = True
        except socket.error:
            ip_valid = False
        #----- check if ip adress is valid -----#
        if ip_valid:

            present_date = datetime.datetime.now()
            ref_date_1 = present_date - datetime.timedelta(days=1)
            ref_date_2 = present_date - datetime.timedelta(days=2)

            if Visitor_Infos.objects.filter(ip_address=ip, page_visited=request.path, event_date__gte=ref_date_1).count() == 0:
                new_visitor_infos = Visitor_Infos(
                ip_address = ip,
                page_visited = request.path,
                event_date = present_date)          
                new_visitor_infos.save()

            if Visitor_Infos.objects.filter(ip_address=ip, page_visited=request.path, event_date__gte=ref_date_1).count() == 1:
                visitor_infos_obj = Visitor_Infos.objects.get(ip_address=ip, page_visited=request.path, event_date__gte=ref_date_1)
                visitor_infos_obj.event_date = present_date
                visitor_infos_obj.save()
    except:
        pass

    context_nb_vistors = 0
    ref_date = present_date - datetime.timedelta(minutes=5) 
    context_nb_vistors = Visitor_Infos.objects.filter(event_date__gte=ref_date).values_list('ip_address', flat=True).distinct().count()

    return {"context_nb_vistors":context_nb_vistors}