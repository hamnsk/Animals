from django.conf.urls import url
from .views import ShowPetListView, ShowShelterListView

urlpatterns = [
    url(r'^pets/', ShowPetListView.as_view()),
    url(r'^shelters/', ShowShelterListView.as_view()),
]