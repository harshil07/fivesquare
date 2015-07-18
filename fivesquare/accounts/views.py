from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from mongoengine.django.auth import User
from mongoengine.queryset import DoesNotExist

def login_view(request):
    if request.method == "GET":
        return render(request, "login.html", {})
    else:
        try:
            user = User.objects.get(username=request.POST['username'])
            if user.check_password(request.POST['password']):
                user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                login(request, user)
                request.session.set_expiry(60 * 60 * 1) # 1 hour timeout
                return HttpResponseRedirect('/api/business/')
            else:
                return HttpResponse('login failed')
        except DoesNotExist:
            return HttpResponse('user does not exist')
        except Exception:
            return HttpResponse('unknown error')

