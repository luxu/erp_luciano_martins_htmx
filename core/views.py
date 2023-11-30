# from django.contrib.auth.models import User
from accounts.models import User
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_protect
# from .serializers import UserSerailizer

import json

# @csrf_protect
# def userSettings(request):
#     user, created = User.objects.get_or_create(id=1)
#     setting = user.setting
#     seralizer = UserSerailizer(setting, many=False)
#     return JsonResponse(seralizer.data, safe=False)

def update_theme(request):
    data = json.loads(request.body)
    theme = data['theme']

    user, created = User.objects.get_or_create(id=1)
    user.setting.value = theme
    user.setting.save()
    print('Request:', theme)
    return JsonResponse('Updated..', safe=False)
