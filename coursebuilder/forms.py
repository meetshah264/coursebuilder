from django import forms
from .models import Course, Grade, Assignment, Events
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
  email = forms.EmailField(
    max_length=254,
    help_text='Required. Enter a valid email address.',
  )

  class Meta:
    model = User
    fields = ('username', 'email')
  
class ForgotPasswordForm(forms.Form):
  username = forms.CharField(max_length=100)
  email = forms.EmailField()
  password = forms.CharField(widget=forms.PasswordInput)

class CourseForm(forms.ModelForm):
  class Meta:
    model = Course
    fields = ['title', 'description']

class GradeStudentForm(forms.ModelForm):  
  class Meta:
    model = Grade
    fields = ['course', 'assignment']

  course = forms.ModelChoiceField(
    queryset=Course.objects.all(), label='Course'
  )

  assignment = forms.ModelChoiceField(
    queryset=Assignment.objects.all(), label='Assignment'
  )

class EventForm(forms.ModelForm):
  class Meta:
    model = Events
    fields = ['title', 'description']

class GradeForm(forms.ModelForm):  
  class Meta:
    model = Grade
    fields = ['user','course', 'assignment', 'grade']

class AssignmentForm(forms.ModelForm):
  class Meta:
    model = Assignment
    fields = ['title', 'description', 'due_date', 'file']


