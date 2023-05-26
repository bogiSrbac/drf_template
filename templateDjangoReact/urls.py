"""

"""

from django.urls import path
from . import views


app_name = 'templateDjangoReact'


urlpatterns = [
    path('mydata/', views.MyDataView.as_view(), name='myData'),
]