from django.conf.urls import url, include
from project.api import views

urlpatterns = [
    url(r'^user/', views.User.as_view()),
    url(r'^freebieRequest/', views.FreebieRequest.as_view()),
]
