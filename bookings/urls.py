from django.urls import path
from bookings import views

app_name = 'lesson'

urlpatterns = [
    # /api/booking/
    path('', views.LessonDayArchiveView.as_view()),

    # /api/booking/5
    # path('<int:pk>/', views.BookingDetail.as_view()),
]
