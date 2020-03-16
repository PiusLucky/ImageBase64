import os
import base64
import requests
import re
import urllib.request
import posixpath
from django.shortcuts import render 
from rest_framework import generics
from .serializers import LinkSerializer, LinkDecodeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from main.models import Link_Model, Field_Model
from main.logic import humanbytes
from main.forms import LinkUpload, LinkDecodeForm
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
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status

# This should take the domain(or sub-domain) upon production
domain_name = settings.DOMAIN_NAME 
name = settings.SITE_NAME
image_formats = ("image/png", "image/jpeg", "image/jpg", "image/webp", "image/gif")




def deletefunc():
    all_files = Link_Model.objects.all()
    for each_file in all_files:
        each_file.delete()
    return {}

def deletedefunc():
    all_files = Field_Model.objects.all()
    for each_file in all_files:
        each_file.delete()
    return {}

class LinkEncodeView(generics.CreateAPIView):
    # Create a new instance of the Link_Model
    queryset = Link_Model.objects.all()
    serializer_class = LinkSerializer
    def post(self, request, format=None):
        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           unique_id = serializer.data["unique_id_link"]
           detail_full_link = u'{0}/api/v1/link/encode/{1}'.format(domain_name, unique_id)
           return HttpResponseRedirect(redirect_to=detail_full_link)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LinkAPIDetailView(APIView):
    def get(self, request, encode_id):
        _encode_id = encode_id
        title = "Link Detail"
        link_id_strip = _encode_id.replace("encoded_link_","")
        specific_link = Link_Model.objects.filter(unique_id_link=link_id_strip)
        link_head_url = settings.ENCODE_URL
        if specific_link:
            for each_item in specific_link:
                formatedDate = each_item.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    url = each_item.url       
                    r = requests.head(url)
                    if r.headers["content-type"] in image_formats:
                        extension = r.headers["content-type"]
                        image_extension = extension.split("/")[-1]
                        #Getting imagename
                        urlpath = urlsplit(url).path
                        basename = posixpath.basename(unquote(urlpath))
                        if (os.path.basename(basename) != basename or
                        unquote(posixpath.basename(urlpath)) != basename):
                            template = "Strange Link: URL provided could not be read properly, try another URL."
                            context = {
                            "title":title,
                            "name":name,
                            "error_message":template,
                            }
                            return Response(context, status=status.HTTP_409_CONFLICT)
                        if str(image_extension) in basename: 
                            new_image_name = basename.replace("." + str(image_extension), "")
                            image_name_without_extension = new_image_name
                            image_name_with_extension = image_name_without_extension + ".{0}".format(image_extension)
                            image_name_with_txt_extension = image_name_without_extension + ".txt"
                            second_part = requests.get(url).content
                            filenamex =  image_name_with_extension
                            r = requests.get(url, allow_redirects=False)
                            full_file_path = os.path.join(settings.ENCODE_ROOT, str(filenamex))
                            with open(str(full_file_path), 'wb+') as f:
                                f.write(r.content)
                            # Removing all other files (that are of image extensions only) 
                            # in the directory except the specified
                            for each_file in os.listdir(str(settings.ENCODE_ROOT)):
                            # Since we needed the extension to take a lower case, we split as follows
                                if "." in each_file:
                                    each_file_extension = each_file.split(".")[-1]
                                    each_file_extension_lower = each_file_extension.lower()
                                    if each_file_extension_lower:
                                        str_extension = "." + str(each_file_extension_lower)
                                        file_name_without_extension = filenamex.replace(str_extension, "") 
                                        if each_file_extension_lower == "jpg" or  each_file_extension_lower == "txt"  or each_file_extension_lower == "jpeg" or each_file_extension_lower == "png" or each_file_extension_lower == "webp" or each_file_extension_lower == "gif":
                                            # This removes otherfiles except the current
                                            if not file_name_without_extension in each_file:
                                                full_path_remove =  os.path.join(settings.ENCODE_ROOT, str(each_file))
                                                os.remove(full_path_remove)

                            width, height = Image.open(full_file_path).size
                            image_dimension = (u"{0} x {1}".format(width, height))
                            # Getting file size using logic in logic.py
                            image_size = os.path.getsize(full_file_path)
                            # lets authenticate the size of the image here
                            maximum_size_image= 1048576 # This is 1MB in bytes
                            # Converting Bytes
                            converted_byte = humanbytes(image_size)
                            if image_size < maximum_size_image:
                                with open(full_file_path, 'wb+') as image:
                                    image.write(second_part)
                                # Getting the base64 string
                                with open(full_file_path, "rb+") as x:
                                # This is the string that is transformed to image
                                    wierdo_string = base64.b64encode(x.read())
                                    # Not really the code that is transformed to image
                                    extension = full_file_path.split(".")[-1]
                                    full_base64 = u"data:image/{0};base64,{1}".format(extension, wierdo_string).replace("b'", "").replace("'","")

                                txt_path = os.path.join(settings.ENCODE_ROOT, str(image_name_with_txt_extension))
                                with open(str(txt_path), 'w+') as f:
                                    f.write(full_base64)
                                    f.close()

                                with open(full_file_path, "rb+") as image_file:
                                    encoded_string = base64.b64encode(image_file.read())
                                image_data = base64.b64decode(encoded_string)
                                filename = full_file_path
                                with open(filename, 'wb') as f:
                                    f.write(image_data)
                                # delete call...
                                all_links = Link_Model.objects.all().exclude(unique_id_link=link_id_strip)
                                # Delete all other images excluding the current one.
                                for each_link in all_links:
                                    each_link.delete()
                            else:
                                # remove all files from database
                                deletefunc()
                                # remove all files from the encode directory as well
                                for each_file in os.listdir(str(settings.ENCODE_ROOT)):
                                    full_path_remove =  os.path.join(settings.ENCODE_ROOT, str(each_file))
                                os.remove(full_path_remove)
                                image_size_formatted = humanbytes(image_size)
                                maximum_size_formatted = humanbytes(maximum_size_image)
                                response = u' Image size {0} exceeds the max of {1}'.format(image_size_formatted, maximum_size_formatted)
                                template = u'file size too large: {0}'.format(response)
                                context = {
                                "title":title,
                                "name":name,
                                "error_message":template,
                                }
                                return Response(context, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
                        # if image extension not in name - a case of conflict b/w jpeg/jpg
                        else:
                            if image_extension == "jpeg":
                                image_extension = "jpg"
                                new_image_name = basename.replace("." + str(image_extension), "")
                                image_name_without_extension = new_image_name
                                image_name_with_extension = image_name_without_extension + ".{0}".format(image_extension)
                                image_name_with_txt_extension = image_name_without_extension + ".txt"
                                second_part = requests.get(url).content
                                filenamex =  image_name_with_extension
                                r = requests.get(url, allow_redirects=False)
                                full_file_path = os.path.join(settings.ENCODE_ROOT, str(filenamex))
                                with open(str(full_file_path), 'wb+') as f:
                                    f.write(r.content)
                                # Removing all other files (that are of image extensions only) 
                                # in the directory except the specified
                                for each_file in os.listdir(str(settings.ENCODE_ROOT)):
                                # Since we needed the extension to take a lower case, we split as follows
                                    if "." in each_file:
                                        each_file_extension = each_file.split(".")[-1]
                                        each_file_extension_lower = each_file_extension.lower()
                                        if each_file_extension_lower:
                                            str_extension = "." + str(each_file_extension_lower)
                                            file_name_without_extension = filenamex.replace(str_extension, "") 
                                            if each_file_extension_lower == "jpg" or  each_file_extension_lower == "txt"  or each_file_extension_lower == "jpeg" or each_file_extension_lower == "png" or each_file_extension_lower == "webp" or each_file_extension_lower == "gif":
                                                # This removes otherfiles except the current
                                                if not file_name_without_extension in each_file:
                                                    full_path_remove =  os.path.join(settings.ENCODE_ROOT, str(each_file))
                                                    os.remove(full_path_remove)

                                width, height = Image.open(full_file_path).size
                                image_dimension = (u"{0} x {1}".format(width, height))
                                # Getting file size using logic in logic.py
                                image_size = os.path.getsize(full_file_path)
                                # lets authenticate the size of the image here
                                maximum_size_image= 1048576 # This is 1MB in bytes
                                # Converting Bytes
                                converted_byte = humanbytes(image_size)
                                if image_size < maximum_size_image:
                                    with open(full_file_path, 'wb+') as image:
                                        image.write(second_part)
                                    # Getting the base64 string
                                    with open(full_file_path, "rb+") as x:
                                    # This is the string that is transformed to image
                                        wierdo_string = base64.b64encode(x.read())
                                        # Not really the code that is transformed to image
                                        extension = full_file_path.split(".")[-1]
                                        full_base64 = u"data:image/{0};base64,{1}".format(extension, wierdo_string).replace("b'", "").replace("'","")
                                        css_base64 = u"url({0})".format(full_base64)
                                        download_link = u"{0}{1}{2}".format(domain_name, link_head_url, image_name_with_extension)
                                    txt_path = os.path.join(settings.ENCODE_ROOT, str(image_name_with_txt_extension))
                                    with open(str(txt_path), 'w+') as f:
                                        f.write(full_base64)
                                        f.close()

                                    with open(full_file_path, "rb+") as image_file:
                                        encoded_string = base64.b64encode(image_file.read())
                                    image_data = base64.b64decode(encoded_string)
                                    filename = full_file_path
                                    with open(filename, 'wb') as f:
                                        f.write(image_data)
                                    # delete call...
                                    all_links = Link_Model.objects.all().exclude(unique_id_link=link_id_strip)
                                    # Delete all other images excluding the current one.
                                    for each_link in all_links:
                                        each_link.delete()
                                else:
                                    # remove all files from database
                                    deletefunc()
                                    # remove all files from the encode directory as well
                                    for each_file in os.listdir(str(settings.ENCODE_ROOT)):
                                        full_path_remove =  os.path.join(settings.ENCODE_ROOT, str(each_file))
                                    os.remove(full_path_remove)
                                    image_size_formatted = humanbytes(image_size)
                                    maximum_size_formatted = humanbytes(maximum_size_image)
                                    response = u' Image size {0} exceeds the max of {1}'.format(image_size_formatted,maximum_size_formatted)
                                    template = u'file size too large: {0}'.format(response)
                                    context = {
                                    "title":title,
                                    "name":name,
                                    "error_message":template,
                                    }
                                    return Response(context, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

                    else:
                        deletefunc()
                        template = "Invalid URL Format URL does not contain any of the image formats allowed (i.e png, jpeg/jpg, webp, gif)"
                        context = {
                        "title":title,
                        "name":name,
                        "error_message":template,
                        }
                        return Response(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
                        # return Response(context)
                except:
                    deletefunc()
                    template = "Network Error: The link could not be accessed. Try again!"
                    context = {
                                "title":title,
                                "name":name,
                                "error_message":template,
                            }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
        else:
            deletefunc()
            msg = "Dead Link Error: The link inputted is a dead link. Try again!"
            context = {
            "title":title,
            "name":name,
            "error_message":msg,
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
                                         
        context = {
                    "title":title,
                    "name":name,
                    "time_encoded":formatedDate,
                    "encode_id":_encode_id,
                    # "image_name_with_txt_extension":image_name_with_txt_extension,
                    # "file":specific_link,
                    "image_info": {
                        "image_extension":image_extension,
                        "image_name":image_name_without_extension,
                        "image_dimension":image_dimension,
                        "image_size":converted_byte,
                    },
                    "raw_copy_base64":full_base64,
                    "css_copy_base64":css_base64,
                    "download_link":download_link,

                    }
        return Response(context)



class LinkDecodeView(generics.CreateAPIView):
    # Create a new instance of the Link_Model_Decode
    queryset = Field_Model.objects.all()
    serializer_class = LinkDecodeSerializer
    def post(self, request, format=None):
        serializer = LinkDecodeSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           unique_id = serializer.data["unique_id_paste"]
           detail_full_link = u'{0}/api/v1/link/decode/{1}'.format(domain_name, unique_id)
           print(detail_full_link)
           return HttpResponseRedirect(redirect_to=detail_full_link)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LinkDecodeDetailView(APIView):
    def get(self, request, unique_id_paste):
        title ="PasteDetail"
        paste_head_url = settings.PASTE_URL
        try:
            specific_file = Field_Model.objects.filter(unique_id_paste = unique_id_paste)
            get_specific = get_object_or_404(Field_Model, unique_id_paste=unique_id_paste)
            paste_id = get_object_or_404(Field_Model, unique_id_paste=unique_id_paste).unique_id_paste
            paste_id_custom = paste_id.replace("id_", "")
            formatedDate = get_object_or_404(Field_Model, unique_id_paste=unique_id_paste).timestamp
            formatedDate = formatedDate.strftime("%Y-%m-%d %H:%M:%S")
            # Specific file was a queryset, we have to convert to string
            string_form_paste = specific_file[0]
            word_count = 1000
            initial_prefix = re.findall("^data.*?,", str(string_form_paste)) 
            stringified = str(string_form_paste) 
            if initial_prefix and len(stringified) >= word_count:
                initial_prefix = initial_prefix[0] # Extracting the first & only element in the list
                raw_line = stringified.replace(str(initial_prefix), "")
                image_data = base64.b64decode(raw_line)
                # Creating dynamic file extension
                extension = initial_prefix.split(";")[0].split("/")[-1]
                file_name = "converted_image_{0}.png".format(paste_id) # Just a placeholder
                file_txt = "converted_image_{0}.txt".format(paste_id)
                file_path = os.path.join(settings.PASTE_ROOT, str(file_name))
                file_path_extension = file_path.split(".")[-1]
                new_file_path = file_path.replace(file_path_extension, extension)
                with open(str(new_file_path), 'wb+') as f:
                    f.write(image_data)
                f.close()
                for each_file in os.listdir(str(settings.PASTE_ROOT)):
                    # Since we needed the extension to take a lower case, we split as follows
                        # delete call...
                    all_files = Field_Model.objects.all().exclude(unique_id_paste=unique_id_paste)
                    # Delete all other images excluding the current one.
                    for each_file in all_files:
                        each_file.delete()
                    # Remaining files
                    r_files = Field_Model.objects.filter(unique_id_paste = unique_id_paste)
                    # Grabbing file header url
                    file_head_url = settings.PASTE_URL
                    # Concatenating full converted image name  
                    full_image_name = u"converted_image_{0}.{1}".format(paste_id, extension)
                    image_name_without_extension = u"converted_image_{0}".format(paste_id)
                    # Getting image dimension and size
                    full_image_link = "{0}{1}{2}".format(domain_name, file_head_url, full_image_name)
               
                    with Image.open(urllib.request.urlopen(full_image_link)) as im:
                        width, height = im.size
                        image_dimension = (u"{0} x {1}".format(width, height))
                        width_adjusted = width + 70
                        height_adjusted = height + 70
                    
                    for each_file in os.listdir(str(settings.PASTE_ROOT)):
                        if u"converted_image_{0}.{1}".format(paste_id, extension) in each_file:    
                            image_full_path = os.path.join(settings.PASTE_ROOT, str(each_file)) 
                            image_size = os.path.getsize(image_full_path)
                            # # Converting Bytes
                            converted_byte = humanbytes(image_size)
                        # Delete unnecessary files from folder
                        if not image_name_without_extension in each_file:
                            full_path_remove =  os.path.join(settings.PASTE_ROOT, str(each_file))
                            with open(str(full_path_remove), 'r') as f:
                                f.close()
                            os.remove(full_path_remove)
                            
            else:
                deletedefunc()
                msg = "Invalid Base64 Error: Sorry, Invalid Base64 string. Try again!"
                context = {
                "title":title,
                "name":name,
                "error_message":msg,
                }
                return Response(context, status=status.HTTP_400_NOT_FOUND)
        except:
            deletedefunc()
            msg = "Page not found!"
            context = {
            "title":title,
            "name":name,
            "error_message":msg,
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        download_link = u'{0}{1}{2}'.format(domain_name, paste_head_url, full_image_name)
        context = {
        "title": title,
        "name": name,
        "time_encoded": formatedDate,
        "unique_id_paste": paste_id,
        "image_info": {
            "image_extension": extension,
            "generated_image_name": full_image_name,
            "image_dimension": image_dimension,
            "image_size" : converted_byte,
        },
        "download_link":download_link,
        "html_image":u'<img src="{0}" alt="Image with ID {1}" />'.format(download_link, paste_id_custom),
        }
        return Response(context)