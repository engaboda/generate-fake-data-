from django.urls import path 
from . import views

app_name='duplicate'
urlpatterns =[
    path('duplicate_row/' , views.duplicate_row , name='duplicate_row'),
    path('fake_data/' , views.fake_data , name='fake_data'),
]