import requests
from main.utils import generate_session_id
from main.models import Update_Model
from django.conf import settings
from django.shortcuts import render



name = settings.SITE_NAME


def landing(request):
    session_key = request.session.session_key
    request.session.modified = True
    if not session_key is None:
        request.session["session_key"] = session_key
        key = session_key[0:8]
        key_upper = key.upper()
        mlist = []       
        for key, val in request.session.items():
            if session_key == val:
                mlist.append(val)
        delimiter = ''
        # // since value are all basically same, pick the first
        mlist = mlist[0]
        old_session_key = delimiter.join(mlist)
        if session_key == old_session_key:
            track = 'old_user'
            message = "Welcome Back, We missed you!"
            track_anonymous = "none"
            status = "Public"
        else:
            track = 'new_user'
            message = "New User (Read the Guide)"
            track_anonymous = "none"
            status = "Public"
    else:
        #Tracking private browsers
        new_list = []
        # if there is no session key, do inject into it.
        request.session['session_key'] = generate_session_id()
        for key, val in request.session.items():
            new_list.append(val)
        delimiter = ''
        new_list = new_list[0]
        old_session_key = delimiter.join(new_list)
        key = old_session_key[0:8]
        key_upper = key.upper()
        if old_session_key:
            track = 'new_user'
            track_anonymous = "set"
            status = "Private"
            message = "Using Private Browser"
    
    return {
    "track":track,
    "message_track":message,
    "track_anonymous":track_anonymous,
    "status":status,
    "visitor_id":key_upper,
    }


def update(request):
    specific_update = Update_Model.objects.filter(authenticate='PiusLucky')
    return {
    "updates":specific_update,
    }


