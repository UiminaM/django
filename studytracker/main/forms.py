from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Student, Submission, Assignment

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['email', 'name', 'password']

class StudentLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")



class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'course', 'deadlain', 'file_assignment']


class AssignmentEditForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'course', 'deadlain', 'file_assignment']

class SubmissionEditForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade', 'submitted_at']