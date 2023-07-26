from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='recruiter_home'),
    path('resume/<str:applicantId>', views.resume, name='recruiter_resume')
]
