from django.urls import path
from .views import PersonList, PersonDetail, StatsView

urlpatterns = [
    path('person/', PersonList.as_view(), name='person-list'),
    path('person/<int:pk>/', PersonDetail.as_view(), name='person-detail'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('person/delete/', PersonList.as_view(), name='person-delete'),
]
