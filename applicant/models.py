from email.policy import default
from django.db import models

class Applicant(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=25)
    file = models.FileField(upload_to='resumes/')
    processed_resume = models.CharField(max_length=5_000)
    status = models.CharField(max_length=50, default='under_consideration')

    def __str__(self):
        return self.name