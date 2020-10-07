from django.shortcuts import render
from rest_framework import generics
from .models import Lesson
from .serializers import LessonSerializer
from django.views.generic.dates import DayArchiveView


class LessonDayArchiveView(DayArchiveView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    date_field = "date"
    # year_format =ㅋ
    allow_future = True

    # def get_queryset(self):
    #     date = self.request.query_params.get('date')
    #     return Lesson.objects.filter(date=date)
