import ast
from multiprocessing import context
from django.shortcuts import render
from applicant.models import Applicant

def home(request):
    context = {
        'applicants' : Applicant.objects.filter(status='under_consideration')
    }

    return render(request, 'recruiter/home.html', context)

def resume(request, applicantId):
    applicant = Applicant.objects.get(id=applicantId)
    resume = applicant.processed_resume
    resume = ast.literal_eval(resume)
    resume_dict = {}
    print(resume['Applicant Information'][1:])

    context = {
        'applicant' : resume['Applicant Information'][1:]
    }

    return render(request, 'recruiter/resume.html', context)