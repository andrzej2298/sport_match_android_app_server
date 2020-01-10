from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from .models import User, Workout


def index(request):
    return JsonResponse({
        'hello': 'world'
    })


def users(request):
    all_users = serialize('json', User.objects.all())
    return HttpResponse(all_users, content_type='application/json')


def workouts(request):
    all_workouts = serialize('json', Workout.objects.all(), use_natural_foreign_keys=True)
    return HttpResponse(all_workouts, content_type='application/json')
