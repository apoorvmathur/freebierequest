from django.conf.urls import url, include
from project.api import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^user/', views.User.as_view()),
    url(r'^request/', views.FreebieRequest.as_view()),
    url(r'^update/', views.Approval.as_view()),
    url(r'^insert/', views.Insert.as_view()),
    url(r'^agents/', views.Agents.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)