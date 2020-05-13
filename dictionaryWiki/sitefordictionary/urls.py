from . import views
from django.urls import path

urlpatterns = [

    path("",views.index, name="index"),
    path("addwords",views.addWords, name="addWords"),
    path("viewword/<int:wordID>",views.viewWord,name="viewWord")

]
