from django.urls import path
from . import views

app_name = 'classify_app'
urlpatterns = [
    path('', views.img_up, name='img_up'),
    # path('transform/', views.transform, name='transform'),
]
