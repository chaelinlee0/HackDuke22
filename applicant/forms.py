from django.forms import ModelForm
from .models import Applicant

class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        fields = ['name', 'email', 'phone', 'file']