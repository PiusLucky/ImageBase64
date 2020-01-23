import os
import base64
import requests
import re
import urllib.request


from django.shortcuts import render
from django.urls import reverse
from .models import Image_Model, Link_Model, File_Model, Field_Model, Link_Model_Decode, Update_Model
from .logic import humanbytes
from .forms import UploadForm, LinkUpload, LinkDecodeForm, FieldForm, FileForm
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

# This should take the domain(or sub-domain) upon production
domain_name = settings.DOMAIN_NAME 


name = settings.SITE_NAME


def csrf_byepass(request, reason=""):
    message = "Refresh page before encoding/decoding..."
    template = get_template('main/_csrf_failure.html').render({"csrf_custom":message})
    messages.error(request, template,"alert alert-warning alert-dismissible")
    return redirect(request.META['HTTP_REFERER']) #To return the same page
    


def landing(request):
    title = "LandingPage" 
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
    
    context = {
    "title":title,
    "name":name,
    "track":track,
    "message_track":message,
    "track_anonymous":track_anonymous,
    "status":status,
    "visitor_id":key_upper,
    }
    return render(request,'main/landing.html',context)

########################################################
# ENCODE SECTION BY LUCKY P. (JUST ANOTHER PROGRAMMER)
########################################################
def home(request):
    title = "Encode"
    form = UploadForm(request.POST or None, request.FILES or None)
    form1 = LinkUpload(request.POST or None, request.FILES or None)
    if request.method == 'GET':
        form = UploadForm()
        #this call () clears the form
        form1 = LinkUpload()
    elif request.method == "POST":
        if request.POST.get('get_upload_name') == 'get_upload_value':
            if form.is_valid():           
                instance = form.save(commit=False)
                instance.save()
                context = {
                    "form":form,
                }
                return HttpResponseRedirect(instance.get_absolute_url())
                context = {
                "title":title,
                "name":name,
                "form":form,
                "form1":form1,
                }
            else:
                template = get_template('main/_wrong_file_type.html').render()
                messages.error(request, template,"alert alert-warning alert-dismissible")
                form1 = LinkUpload()
                # if the form is not valid ,the command clears the LinkUpload and leave validation error message present in Upload_Form...
                return render(request, 'main/front_page.html', {     "title": title, 
                "name":name,
                "form":form,
                "form1":form1,
					} )
        elif request.POST.get('get_link_name') == 'get_link_value':
            if form1.is_valid():           
                instance = form1.save(commit=False)
                instance.save()
                context = {
                    "form1":form1,
                }
                return HttpResponseRedirect(instance.get_absolute_url())
                context = {
                "title":title,
                "name":name,
                "form":form,
                "form1":form1,
                }
            else:   
                template = get_template('main/_https_failed.html').render()
                messages.error(request, template,"alert alert-warning alert-dismissible")
                form = UploadForm()
                # if the form is not valid ,the command clears the UploadForm and leave validation error message present in LinkUpload Form...
                return render(request, 'main/front_page.html', {"title": title, 
                "name":name,
                "form":form,
                "form1":form1,
					} )
    else:
        pass
    context =  {"title": title, 
    "name":name,
    "form":form,
    "form1":form1,
     }
    return render(request,'main/front_page.html',context)

def detail(request, id):
    specific_file = Image_Model.objects.filter(id=id)
    media_head_url = settings.MEDIA_URL  
    if specific_file:
        for each_item in specific_file:
            formatedDate = each_item.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            # 2020-01-18 01:22:29
            if each_item.image:
                # Extracting the image name
                # print(each_item.image.name)
                # The above outputs "uploads-image/Waterfall_pu6xTmm.jpg"
                # Now, lets manipulate the result above to extract the name of the image
                long_name = each_item.image.name
                # splitting by "/"
                last_item = long_name.split("/")[-1]
                image_name = last_item      
                # Extracting the image link
                image_url = each_item.image.url
                full_url = domain_name + str(image_url)
        title = "Encode Detail"
        mylink = full_url
        second_part = requests.get(mylink).content
        filenamex =  image_name
        full_path = os.path.join(settings.MEDIA_ROOT, str(filenamex))
        url =  mylink
        r = requests.get(url, allow_redirects=False)
        with open(str(full_path), 'wb+') as f:
            f.write(r.content)
        # Removing all other files (that are of image extensions only) 
        # in the directory except the specified
        for each_file in os.listdir(str(settings.MEDIA_ROOT)):
            # Since we needed the extension to take a lower case, we split as follows
            if "." in each_file:
                file_name = str(filenamex)
                each_file_extension = file_name.split(".")[-1]
                each_file_extension_lower = each_file_extension.lower()
                if each_file_extension_lower:
                    str_extension = "." + str(each_file_extension_lower)
                file_name_without_extension = file_name.replace(str_extension, "") 
                each_file_extension = each_file.split(".")[-1]
                each_file_extension_lower = each_file_extension.lower()
                if each_file_extension_lower:
                    if each_file_extension_lower == "jpg" or each_file_extension_lower == "txt" or each_file_extension_lower == "jpeg" or each_file_extension_lower == "png" or each_file_extension_lower == "webp" or each_file_extension_lower == "gif":
                        # This removes otherfiles except the current
                        if not file_name_without_extension in each_file:
                            full_path_remove =  os.path.join(settings.MEDIA_ROOT, str(each_file))
                            os.remove(full_path_remove)
            width, height = Image.open(full_path).size
            image_dimension = (u"{0} x {1}".format(width, height))
            # image_size = os.path.getsize(filenamex)
            # # Converting Bytes
            # converted_byte = humanbytes(image_size)
            # print(converted_byte)
            with open(full_path, 'wb+') as image:
                image.write(second_part)
        
            # Getting the base64 string
            with open(full_path, "rb") as x:
                # This is the string that is transformed to image
                wierdo_string = base64.b64encode(x.read())
                # Not really the code that is transformed to image
                extension = full_path.split(".")[-1]
                full_base64 = u"data:image/{0};base64,{1}".format(extension, wierdo_string).replace("b'", "").replace("'","")
                
            ########################################
            # Getting full path with ext. 
            ########################################

            path = full_path.split(".")
            wiki = path.pop(len(path)-1)
            ziga = path.append(str(extension))
            part = '.'
            new_file_path = part.join(path)

            ########################################
            # Getting image name with & without ext. 
            ########################################
            # Lets remove the last value of the list
            x = full_path.split(".")
            v = x.pop(len(x)-1)
            # Lets grab the image name without extension
            delimiter = '.'
            w = delimiter.join(x)
            w = w.split("/")
            image_name_without_extension = w[-1]
            x.append(str(extension))
            # Converting the above list to string
            delimiter = '.'
            w = delimiter.join(x)
            w = w.split("/")
            image_name_with_extension = w[-1]
            image_name_with_txt_extension = image_name_without_extension + ".txt"
            full_image_name = image_name_with_extension

            txt_path = os.path.join(settings.MEDIA_ROOT, str(image_name_with_txt_extension))
            with open(str(txt_path), 'w+') as f:
                f.write(full_base64)
                f.close()

            with open(full_path, "rb+") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            image_data = base64.b64decode(encoded_string)
            filename = filenamex
            with open(full_path, 'wb+') as f:
                f.write(image_data)
            # delete call...
            all_images = Image_Model.objects.all().exclude(id=id)
            # Delete all other images excluding the current one.
            for each_image in all_images:
                each_image.delete()
    else:
        expired_link = "The link has expired!"
        template = get_template('main/_expired_link.html').render({"expired_link":expired_link})
        messages.error(request, template,"alert alert-warning alert-dismissible")
        return redirect(reverse("main:home")) 
    context = {
    "title":title,
    "name":name,
    "formatedDate":formatedDate,
    "media_head_url":media_head_url,
    "base64_output":encoded_string,
    "wierdo_string":full_base64,
    "file":specific_file,
    "image_name":image_name,
    "image_dimension":image_dimension,
    "image_name_with_txt_extension":image_name_with_txt_extension,
    }
    return render(request,'main/detail_page.html',context)

def detail_link(request, encode_id):
    title = "Link Detail"
    # Arrangements doesnt really matter here
    link_id_strip = encode_id.replace("encoded_link_","")
    specific_link = Link_Model.objects.filter(unique_id_link=link_id_strip)
    link_head_url = settings.ENCODE_URL
    if specific_link:
        for each_item in specific_link:
            formatedDate = each_item.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            try:
                url = each_item.url
                if url:          
                    if url.endswith(".jpg") or url.endswith(".png") or url.endswith(".jpeg") or url.endswith(".webp") or url.endswith(".gif"):
                        # http://localhost:8000/media/uploads-image/2020/01/02/CR7.jpg
                        image_name = url.split("/")[-1]
                        if "http://" or "https://" or "www." in url:
                            second_part = requests.get(url).content
                            filenamex =  image_name
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
                                ########################################
                                # Getting full path with ext. 
                                ########################################

                                path = full_file_path.split(".")
                                wiki = path.pop(len(path)-1)
                                ziga = path.append(str(extension))
                                part = '.'
                                new_file_path = part.join(path)

                                ########################################
                                # Getting image name with & without ext. 
                                ########################################
                                # Lets remove the last value of the list
                                x = full_file_path.split(".")
                                v = x.pop(len(x)-1)
                                # Lets grab the image name without extension
                                delimiter = '.'
                                w = delimiter.join(x)
                                w = w.split("/")
                                image_name_without_extension = w[-1]
                                x.append(str(extension))
                                # Converting the above list to string
                                delimiter = '.'
                                w = delimiter.join(x)
                                w = w.split("/")
                                image_name_with_extension = w[-1]
                                image_name_with_txt_extension = image_name_without_extension + ".txt"
                                full_image_name = image_name_with_extension

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
                                all_files = Link_Model.objects.all()
                                for each_file in all_files:
                                    each_file.delete()
                                # remove all files from the encode directory as well
                                for each_file in os.listdir(str(settings.ENCODE_ROOT)):
                                    full_path_remove =  os.path.join(settings.ENCODE_ROOT, str(each_file))
                                os.remove(full_path_remove)
                                image_size_formatted = humanbytes(image_size)
                                maximum_size_formatted = humanbytes(maximum_size_image)
                                response = u' Image size {0} exceeds the max of {1}'.format(image_size_formatted,maximum_size_formatted)
                                template = get_template('main/_wrong_file_size.html').render({"response":response})
                                messages.error(request, template,"alert alert-warning alert-dismissible")
                                return redirect(reverse("main:home"))  
                            
                    else:
                        # if url does not end with any of the provided suffix
                        # delete all the files
                        all_files = Link_Model.objects.all()
                        for each_file in all_files:
                            each_file.delete()
                        template = get_template('main/_invalid_url.html').render()
                        messages.error(request, template,"alert alert-warning alert-dismissible")
                        return redirect(reverse("main:home")) 
            except:
                template = get_template('main/_network_error.html').render()
                messages.error(request, template,"alert alert-warning alert-dismissible")
                return redirect(reverse("main:home"))      
    else:
        template = get_template('main/_dead_link.html').render()
        messages.error(request, template,"alert alert-warning alert-dismissible")
        return redirect(reverse("main:home"))          
    context = {
    "title":title,
    "name":name,
    "formatedDate":formatedDate,
    "image_name_with_txt_extension":image_name_with_txt_extension,
    "link_head_url":link_head_url,
    "file":specific_link,
    "wierdo_string":full_base64,
    "image_name":image_name,
    "image_dimension":image_dimension,
    "converted_byte":converted_byte,
    }
    return render(request,'main/detail_page.html', context)


########################################################
# DECODE SECTION BY LUCKY P. (JUST ANOTHER PROGRAMMER)
########################################################

def home_decode(request):
    title = "Decode" 
    form = LinkDecodeForm(request.POST or None, request.FILES or None)
    form1 = FieldForm(request.POST or None, request.FILES or None)
    form2 = FileForm(request.POST or None, request.FILES or None)
    if request.method == 'GET':
        form = LinkDecodeForm()
        form1 = FieldForm()
        form2 = FileForm()
    elif request.method == "POST":
        if request.POST.get('form_name') == 'form_value':
            if form.is_valid():           
                instance = form.save(commit=False)
                instance.save()
                context = {
                    "form":form,
                }
                return HttpResponseRedirect(instance.get_absolute_url())
                context = {
                "title":title,
                "name":name,
                "form":form,
                "form1":form1,
                "form2":form2,
                }
            else:
                template = get_template('main/_invalid_url.html').render()
                messages.error(request, template,"alert alert-warning alert-dismissible")
                form1 = FieldForm()
                form2 = FileForm()
                return render(request, 'main/front_page_decode.html', { "title": title, 
                "name":name,
                "form":form,
                "form1":form1,
                "form2":form2,
					} )
        elif request.POST.get('form1_name') == 'form1_value':
            form1 = FieldForm(request.POST or None, request.FILES or None)
            if form1.is_valid():           
                instance = form1.save(commit=False)
                instance.save()
                context = {
                    "form1":form1,
                }
                return redirect("main:detail4", instance.unique_id_paste)  
                # return HttpResponseRedirect(instance.get_absolute_url_paste())
                context = {
                "title":title,
                "name":name,
                "form":form,
                "form1":form1,
                "form2":form2,
                }
            else:
                form = LinkDecodeForm()
                form2 = FileForm()
                return render(request, 'main/front_page_decode.html', { "title": title, 
                "name":name,
                "form":form,
                "form1":form1,
                "form2":form2,
					} )
        elif request.POST.get('form2_name') == 'form2_value':
            if form2.is_valid():           
                instance = form2.save(commit=False)
                instance.save()
                context = {
                    "form2":form2,
                }
                return HttpResponseRedirect(instance.get_absolute_url())
                context = {
                "title":title,
                "name":name,
                "form":form,
                "form1":form1,
                "form2":form2,
                }
            else:
                form = LinkDecodeForm()
                form1 = FieldForm()
                return render(request, 'main/front_page_decode.html', { "title": title, 
                "name":name,
                "form":form,
                "form1":form1,
                "form2":form2,
					} )
    else:
        pass
    context =  {"title": title, 
    "name":name,
    "form":form,
    "form1":form1,
    "form2":form2,
     }
    return render(request,'main/front_page_decode.html',context)



def detail_file_decode(request, id, unique_id):
    specific_file = File_Model.objects.filter(id=id, unique_id=unique_id)  
    # if the item is valid
    if specific_file:
        for each_item in specific_file:
            formatedDate = each_item.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            if each_item:
                file_name = each_item
        title = "FileDetail"
        file_path = os.path.join(settings.FILE_ROOT, str(file_name))
        
        # Searching through a file using Prefix
        with open(str(file_path), "r") as file_handle:
            for line in file_handle:
                # x = "data:image/jpg;base64,/9j/4AAQSkZJRgABAQ""
                # output ['data:image/jpg;base64,']
                word_count = 1000
                initial_prefix = re.findall("^data.*?,", line)   
                if initial_prefix and len(line) >= word_count:
                    initial_prefix = initial_prefix[0] # Extracting the first & only element in the list
                    raw_line = line.replace(str(initial_prefix), "")
                    image_data = base64.b64decode(raw_line)

                    # Creating dynamic file extension
                    extension = initial_prefix.split(";")[0].split("/")[-1]
                    file_path_extension = file_path.split(".")[-1]
                    # Resolving conflict (like xx_html.html and xx_png.png) and preventing HTTP Error 404
                    # When calling Image.open(url)
                    # tank.txt.txt
                    
                    ########################################
                    # Getting full path with ext. 
                    ########################################
                    
                    path = file_path.split(".")
                    wiki = path.pop(len(path)-1)
                    ziga = path.append(str(extension))
                    part = '.'
                    new_file_path = part.join(path)

                    ########################################
                    # Getting image name with & without ext. 
                    ########################################
                    # Lets remove the last value of the list
                    x = file_path.split(".")
                    v = x.pop(len(x)-1)
                    # Lets grab the image name without extension
                    delimiter = '.'
                    w = delimiter.join(x)
                    w = w.split("/")
                    image_name_without_extension = w[-1]
                    x.append(str(extension))
                    # Converting the above list to string
                    delimiter = '.'
                    w = delimiter.join(x)
                    w = w.split("/")
                    image_name_with_extension = w[-1]
                    full_image_name = image_name_with_extension

                    with open(str(new_file_path), 'wb+') as f:
                        f.write(image_data)
                    f.close()
                    for each_file in os.listdir(str(settings.FILE_ROOT)):
                        # Since we needed the extension to take a lower case, we split as follows
                        if "." in each_file:
                            file_name = str(file_name)
                            each_file_extension = file_name.split(".")[-1]
                            each_file_extension_lower = each_file_extension.lower()
                            if each_file_extension_lower:
                                # str_extension = "." + str(each_file_extension_lower)
                                # print( "this is extension :" + str(str_extension))
                                # print("filename" + str(file_name))
                                file_name_without_extension = image_name_without_extension
                                # print(file_name_without_extension)
                                # print(extension)
                                if not file_name in each_file:
                                    if not "{0}.{1}".format(file_name_without_extension, extension) in each_file:
                                        fake_path = os.path.join(settings.FILE_ROOT, str(each_file))
                                        open_file = open(fake_path, 'r')
                                        open_file.close()
                                        os.remove(fake_path)
                            # delete call...
                            all_files = File_Model.objects.all().exclude(id=id)
                            # Delete all other images excluding the current one.
                            for each_file in all_files:
                                each_file.delete()
                            # Grabbing file header url
                            file_head_url = settings.FILE_URL                    
                            # Getting image dimension and size
                            full_image_link = "{0}{1}{2}".format(domain_name, file_head_url, full_image_name)

                            with Image.open(urllib.request.urlopen(full_image_link)) as im:
                                width, height = im.size
                            width_adjusted = width + 70
                            height_adjusted = height + 70
                            image_dimension = (u"{0} x {1}".format(width, height))
                            for each_file in os.listdir(str(settings.FILE_ROOT)):
                                if "{0}.{1}".format(file_name_without_extension, extension) in each_file:    
                                    image_full_path = os.path.join(settings.FILE_ROOT, str(each_file)) 
                                    image_size = os.path.getsize(image_full_path)
                                    # # Converting Bytes
                                    converted_byte = humanbytes(image_size)
                                    
                else:
                    for each_item in specific_file:
                        if each_item:
                            file_handle.close() # Close the initial file_handle to prevent Permission Error
                            file_path = os.path.join(settings.FILE_ROOT, str(each_item))
                            open_file = open(file_path, 'r')
                            open_file.close()
                            os.remove(file_path)
                            # delete call... if not valid base64 string delete all objects in the model
                            all_files = File_Model.objects.all()
                            # Delete all other files
                            for each_file in all_files:
                                each_file.delete()
                    template = get_template('main/_invalid_base64.html').render()
                    messages.error(request, template,"alert alert-success alert-dismissible")
                    return redirect(reverse("main:home_decode"))

    else:
        response = "Page not found!"
        template = get_template('main/_not_found.html').render({"response":response})
        messages.error(request, template,"alert alert-warning alert-dismissible")
        return redirect(reverse("main:home_decode"))
    context = {
    "title":title,
    "name":name,
    "file_head_url":file_head_url,
    "file_name":full_image_name,
    "file":specific_file,
    "image_dimension":image_dimension,
    "converted_byte": converted_byte,
    "image_full_path":image_full_path, 
    "formatedDate":formatedDate,
    "domain_name":domain_name,
    "width":width_adjusted,
    "height":height_adjusted,
    }
    return render(request,'main/detail_page_decode.html',context)

   
def detail_paste_decode(request, unique_id_paste):
    title ="PasteDetail"
    try:
        specific_file = Field_Model.objects.filter(unique_id_paste = unique_id_paste)
        get_specific = get_object_or_404(Field_Model, unique_id_paste=unique_id_paste)
        paste_id = get_object_or_404(Field_Model, unique_id_paste=unique_id_paste).unique_id_paste
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
            template = get_template('main/_invalid_base64.html').render()
            messages.error(request, template,"alert alert-success alert-dismissible")
            return redirect(reverse("main:home_decode"))
    except:
        response = "Page not found!"
        template = get_template('main/_not_found.html').render({"response":response})
        messages.error(request, template,"alert alert-warning alert-dismissible")
        return redirect(reverse("main:home_decode"))
    context = {
    "title":title,
    "name":name,
    "file_txt":file_txt,
    "file_head_url":file_head_url,
    "file_name":full_image_name,
    "get_specific":get_specific,
    "paste_id":paste_id,
    "image_dimension":image_dimension,
    "converted_byte": converted_byte,
    "image_full_path":image_full_path, 
    "formatedDate":formatedDate,
    "domain_name":domain_name,
    "width":width_adjusted,
    "height":height_adjusted,
    }
    return render(request,'main/detail_page_decode.html',context)


def detail_link_decode(request, link_id, live_id):
    title = "LinkDecodeDetail"
    # e.g link_16 lets strip it of the extra added letters to
    # derive the original values so we can filter our queryset properly
    link_id_strip = link_id.replace("link_","")
    live_id_strip = live_id.replace("live=","")
    try:
        specific_link = Link_Model_Decode.objects.filter(id=link_id_strip, unique_id_link=live_id_strip)
        if specific_link:
            for each_item in specific_link:
                formatedDate = each_item.timestamp.strftime("%Y-%m-%d %H:%M:%S") 
                try:
                    url = each_item.url
                    if url:
                        if url.endswith(".txt") or url.endswith(".html"):
                            # http://localhost:8000/media/uploads-image/2020/01/02/CR7.txt
                            file_name = url.split("/")[-1]
                            if "http://" or "https://" or "www." in url:
                                second_part = requests.get(url).content
                                filenamex =  file_name
                                full_file_path = os.path.join(settings.LINK_ROOT, str(filenamex))
                                r = requests.get(url, allow_redirects=False)
                                with open(str(full_file_path), 'wb+') as f:
                                        f.write(r.content)
                                
                                # Grab the size of the .txt/.html file
                                file_size = os.path.getsize(full_file_path)
                                file_converted_byte = humanbytes(file_size)
                                # Searching through a file using Prefix
                                file_handle = open(str(full_file_path), "r+")
                                try:
                                    for line in file_handle:
                                    #     # x = "data:image/jpg;base64,/9j/4AAQSkZJRgABAQ""
                                    #     # output ['data:image/jpg;base64,']
                                        word_count = 1000
                                        initial_prefix = re.findall("^data.*?,", line)   
                                        if initial_prefix and len(line) >= word_count:
                                            initial_prefix = initial_prefix[0] # Extracting the first & only element in the list
                                            raw_line = line.replace(str(initial_prefix), "")
                                            image_data = base64.b64decode(raw_line)
                                            # # Creating dynamic file extension
                                            extension = initial_prefix.split(";")[0].split("/")[-1]
                                            file_path_extension = full_file_path.split(".")[-1]
                
                                            ########################################
                                            # Getting full path with ext. 
                                            ########################################

                                            path = full_file_path.split(".")
                                            wiki = path.pop(len(path)-1)
                                            ziga = path.append(str(extension))
                                            part = '.'
                                            new_file_path = part.join(path)
    
                                            ########################################
                                            # Getting image name with & without ext. 
                                            ########################################
                                            # Lets remove the last value of the list
                                            x = full_file_path.split(".")
                                            v = x.pop(len(x)-1)
                                            # Lets grab the image name without extension
                                            delimiter = '.'
                                            w = delimiter.join(x)
                                            w = w.split("/")
                                            image_name_without_extension = w[-1]
                                            x.append(str(extension))
                                            # Converting the above list to string
                                            delimiter = '.'
                                            w = delimiter.join(x)
                                            w = w.split("/")
                                            image_name_with_extension = w[-1]
                                            full_image_name = image_name_with_extension
                                            with open(str(new_file_path), 'wb+') as f:
                                                f.write(image_data)
                                            f.close()
                                    # Removing all other files (that are of image extensions only) 
                                    # in the directory except the specified
                                        for each_file in os.listdir(str(settings.LINK_ROOT)):
                                            # Since we needed the extension to take a lower case, we split as follows
                                                # delete call...
                                            all_files = Link_Model_Decode.objects.all().exclude(id=link_id_strip, unique_id_link=live_id_strip)
                                            # Delete all other images excluding the current one.
                                            for each_file in all_files:
                                                each_file.delete()
                                            # Remaining files
                                            r_files = Link_Model_Decode.objects.filter(id=link_id_strip, unique_id_link=live_id_strip)
                                            # Grabbing file header url
                                            link_head_url= settings.LINK_URL
                                            # # Concatenating full converted image name 
                                            file_name = str(filenamex)
                                            each_file_extension = file_name.split(".")[-1]
                                            each_file_extension_lower = each_file_extension.lower()
                                            if each_file_extension_lower:
                                            # Getting image dimension and size
                                                full_image_link = "{0}{1}{2}".format(domain_name, link_head_url, full_image_name)
                                            with Image.open(urllib.request.urlopen(full_image_link)) as im:
                                                width, height = im.size
                                            image_dimension = (u"{0} x {1}".format(width, height))
                                            width_adjusted = width + 70
                                            height_adjusted = height + 70
                                        for each_file in os.listdir(str(settings.LINK_ROOT)):
                                            if not image_name_without_extension in each_file:
                                                full_path_remove =  os.path.join(settings.LINK_ROOT, str(each_file))
                                                os.remove(full_path_remove)
                                            if u"{0}".format(full_image_name) in each_file:   
                                                image_full_path = os.path.join(settings.LINK_ROOT, str(each_file)) 
                                                image_size = os.path.getsize(image_full_path)
                                                # # Converting Bytes
                                                converted_byte = humanbytes(image_size)
                                                maximum_size_image= 1048576 # This is 1MB in bytes
                                                if image_size > maximum_size_image:
                                                    image_size_formatted = converted_byte
                                                    maximum_size_formatted = humanbytes(maximum_size_image)
                                                    response = u' Link contains image size {0} which exceeds the max of {1}'.format(image_size_formatted,maximum_size_formatted)
                                                    template = get_template('main/_wrong_file_size.html').render({"response":response})
                                                    messages.error(request, template,"alert alert-warning alert-dismissible")
                                                    return redirect(reverse("main:home_decode"))  
                                except:
                                    illegal_request = "File with valid Base64 string not Found!"
                                    template = get_template('main/_illegal_request.html').render({"illegal_request":illegal_request})
                                    messages.error(request, template,"alert alert-warning alert-dismissible")
                                    return redirect(reverse("main:home_decode"))
                        else:
                            invalid_url = "Input url like 'https:abc.com/def.txt or 'http:xyz.net/image_data.html"
                            template = get_template('main/_invalid_url.html').render({"invalid_url":invalid_url})
                            messages.error(request, template,"alert alert-warning alert-dismissible")
                            return redirect(reverse("main:home_decode")) 
                except:
                    template = get_template('main/_dead_link.html').render()
                    messages.error(request, template,"alert alert-warning alert-dismissible")
                    return redirect(reverse("main:home_decode")) 
        else:
            expired_url = "File Expired, Try again."
            template = get_template('main/_invalid_url.html').render({"invalid_url":expired_url})
            messages.error(request, template,"alert alert-warning alert-dismissible")
            return redirect(reverse("main:home_decode")) 
    except:
        template = get_template('main/_dead_link.html').render()
        messages.error(request, template,"alert alert-warning alert-dismissible")
        return redirect(reverse("main:home_decode"))           
    context = {
    "title":title,
    "name":name,
    "file":specific_link,
    "filename":filenamex,
    "image_size":image_size,
    "full_image_name":full_image_name,
    "file_size":file_converted_byte,
    "link_head_url":link_head_url,
    "image_dimension":image_dimension,
    "converted_byte":converted_byte,
    "formatedDate":formatedDate,
    "domain_name":domain_name,
    "width":width_adjusted,
    "height":height_adjusted,
    }
    return render(request,'main/detail_page_decode.html', context)


########################################################
#  UPDATE SECTION BY LUCKY P. (JUST ANOTHER PROGRAMMER)
########################################################

def update(request, update_id):
    title = "UpdateDetail"
    update_id_strip = update_id.replace("update_id_","")
    specific_update = Update_Model.objects.filter(update_id=update_id_strip)
    other_update = Update_Model.objects.exclude(update_id=update_id_strip)
    print(other_update)
    context = {
    "title":title,
    "name":name,
    "update":specific_update,
    "other_update":other_update,
    }
    return render(request,'update/update.html',context)
