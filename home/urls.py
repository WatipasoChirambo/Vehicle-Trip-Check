from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.index,name="index"),
    path("register/",views.register, name="register"),
    path("today/",views.today, name="today"),
    path("yesterday/",views.yesterday, name="yesterday"),
    path("all_week/",views.trips, name="all_week"),
    path('accounts/', include("django.contrib.auth.urls")),
    path('trips/',views.trips,name="trips"),
    path('update/<str:pk>', views.update, name="update"),
    path('trip/<int:pk>', views.trip, name='trip'),
    path('history', views.history,name='history')
]
