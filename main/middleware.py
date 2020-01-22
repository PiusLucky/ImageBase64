from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.core.exceptions import RequestDataTooBig
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.template.loader import get_template
from main.logic import humanbytes


class RequestDataTooBigMiddleware(MiddlewareMixin):
    # NOTE: If the request body is too big then request.body will throw a
    #       RequestDataTooBig exception. Check here explicitly if that will happen.
    #       If we did not check here then a subsequent middleware would crash
    #       and process_exception() would never get called.
    def process_request(self, request):
        try:
            request.body
        except RequestDataTooBig as e:
            response = self.process_exception(request, e)
            if response is not None:
                # return response
                one_mb_pad = 1048576
                max_size_settings = int(settings.DATA_UPLOAD_MAX_MEMORY_SIZE)
                max_diff = max_size_settings - one_mb_pad
                max_size = humanbytes(max_diff)
                response = u"Image file must never exceed {0}".format(max_size)
                template = get_template('main/_wrong_file_size.html').render({"response":response})
                messages.error(request, template,"alert alert-warning alert-dismissible")
                return redirect(request.META['HTTP_REFERER'])
            else:
                # Crash further down in the middleware stack
                pass

        return None

    def process_exception(self, request, exception):
        if isinstance(exception, RequestDataTooBig):
            return HttpResponse(status=200)  # Payload Too Large
        return None