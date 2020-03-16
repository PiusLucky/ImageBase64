from django.shortcuts import render

# Create your views here.

# MainAPIView,
# LinkAPIView,
# FileAPIView,
# FieldAPIView,
# LinkDecodeAPIView 
from rest_framework import generics

from main.models import    (Image_Model,
                            Link_Model,
                            File_Model,
                            Field_Model,
                            Link_Model_Decode,
                            )

from .serializers import   (MainSerializer,
                            LinkSerializer,
                            FileSerializer,
                            FieldSerializer,
                            LinkDecodeSerializer)
import os
import base64
import requests
import re
import urllib.request
import posixpath
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from main.models import Image_Model, Link_Model, File_Model, Field_Model, Link_Model_Decode, Update_Model, Faq_Model, My_Contact_Model, Contact_Me_Model
from main.logic import humanbytes
from main.forms import UploadForm, LinkUpload, LinkDecodeForm, FieldForm, FileForm, Contact_Me_Form
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from PIL import Image
from django.http import JsonResponse
from datetime import datetime
from main.utils import generate_session_id
from urllib.parse import urlsplit, unquote

from rest_framework.views import APIView
from rest_framework.response import Response

class MainAPIView(APIView):
    queryset = Image_Model.objects.all()
    serializer_class = MainSerializer
    template_name = 'main/front_page.html'
    title = "Encode"
    def post(self, request, *args, **kwargs):
        list_url = []
        form = UploadForm(request.POST or None, request.FILES or None)
        if form.is_valid():   
            print("Form is valid")     
            instance = form.save(commit=False)
            instance.save()
            a = instance.get_absolute_url()
            list_url.append(a)
            return Response(instance.get_absolute_url())              
        else:
            print("Form is not valid")
            # template = get_template('main/_wrong_type.html').render()
            # messages.error(request, template,"alert alert-warning alert-dismissible")
            # form1 = LinkUpload()
            # # if the form is not valid ,the command clears the LinkUpload and
            # # leave validation error message present in Upload_Form...
            # return render(request, self.template_name, {
            # "name": name, 
            # "title":self.title,
            # "form":self.form,
            # "form1":self.form1,
                # } )
        context = { 
        "title":self.title,
        "url":list_url
        }
        return Response(context)

        # elif request.POST.get('get_link_name') == 'get_link_value':
        #     form1 = LinkUpload(request.POST or None, request.FILES or None)
        #     if form1.is_valid():           
        #         instance = form1.save(commit=False)
        #         instance.save()
        #         context = {
        #             "form1":form1,
        #         }
        #         return HttpResponseRedirect(instance.get_absolute_url())
        #         context = {
        #         "name": name, 
        #         "title":self.title,
        #         "form":self.form,
        #         "form1":self.form1,
        #         }
        #     else:   
        #         template = get_template('main/_https_failed.html').render()
        #         messages.error(request, template,"alert alert-warning alert-dismissible")
        #         form = UploadForm()
        #         # if the form is not valid ,the command clears the UploadForm and leave validation 
        #         # error message present in LinkUpload Form...
        #         return render(request, self.template_name, {
        #             "name": name, 
        #             "title":self.title,
        #             "form":form,
        #             "form1":self.form1,
        #             } )

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)


class MainAPIViewDetail(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Image_Model.objects.all()
    serializer_class = MainSerializer


class LinkAPIViewDetail(generics.RetrieveAPIView):
    lookup_field = 'unique_id_link'
    queryset = Link_Model.objects.all()
    serializer_class = LinkSerializer
    def get(self, request, *args, **kwargs):
        context = { 
        "title":"Hello",
        "url":"wwww.google.com"
        }
        return Response(context)


