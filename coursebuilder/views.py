from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import EventForm, CourseForm, AssignmentForm, GradeForm, GradeStudentForm, ForgotPasswordForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
import pdb
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, TemplateView

@login_required
def home(request):
    courses = Course.objects.all()
    user = UserProfile.objects.get(user_ptr=request.user.id)
    if user.is_professor:
        return render(request, 'home.html', {'courses': courses})
    else:
        return render(request, 'home_student.html', {'courses': courses})

def signup(request):
  if request.method == 'POST':
      form = SignUpForm(request.POST)
      if form.is_valid():
          user = form.save()
          login(request, user)
          return redirect('home')
  else:
      form = SignUpForm()
  return render(request, 'signup.html', {'form': form})

def course_list(request):
    courses = Course.objects.all()
    # pdb.set_trace()
    user = UserProfile.objects.get(user_ptr=request.user.id)
    if user.is_professor:
        return render(request, 'course_list.html', {'courses': courses})
    else:
        return render(request, 'course_list_student.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = UserProfile.objects.get(user_ptr=request.user.id)
    if user.is_professor:
        return render(request, 'course_detail.html', {'course': course})
    else:
        return render(request, 'course_detail_student.html', {'course': course, 'user': user})

def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})

def course_update(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_form.html', {'form': form, 'course': course})

def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'course_confirm_delete.html', {'course': course})

def assignment_delete(request, course_id, assignment_id):
    course = get_object_or_404(Course, id=course_id)
    courseid = course_id
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignment_list', course_id=courseid)
    return render(request, 'course_confirm_delete.html', {'assignment': assignment})

def assignment_detail(request, course_id, assignment_id):
    course = get_object_or_404(Course, id=course_id)
    assignment = get_object_or_404(Assignment, id=assignment_id)
    user = UserProfile.objects.get(user_ptr=request.user.id)
    if user.is_professor:
        return render(request, 'assignment_detail.html', {'assignment': assignment})
    else:
        return render(request, 'assignment_detail_student.html', {'assignment': assignment})

def assignment_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    assignments = Assignment.objects.filter(course=course)
    user = UserProfile.objects.get(user_ptr=request.user.id)
    if user.is_professor:
        return render(request, 'assignment_list.html', {'course': course, 'assignments': assignments})
    else:
        return render(request, 'assignment_list_student.html', {'course': course, 'assignments': assignments})
        
def assignment_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            return redirect('assignment_list', course_id=course.id)
    else:
        form = AssignmentForm()
    return render(request, 'assignment_form.html', {'form': form, 'course': course})

def assignment_download(request, course_id, assignment_id):
    course = Course.objects.get(id=course_id)
    assignment = Assignment.objects.get(id=assignment_id)
    response = FileResponse(assignment.file)
    response['Content-Disposition'] = f'attachment; filename="{assignment.file.name}"'
    return response

def assignment_update(request, course_id, assignment_id):
    course = get_object_or_404(Course, id=course_id)
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_detail', course_id=course.id, assignment_id=assignment.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'assignment_form.html', {'form': form, 'assignment': assignment})


def login_here(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password') 
    user = authenticate(request, username=username, password=password)
    # pdb.set_trace()
    if user is not None:
      if user.is_active:
        login(request, user)
        return HttpResponseRedirect(reverse('home'))
      else:
        return HttpResponse('Your account is disabled')
    else:
      return HttpResponse('Login details are incorrect')
  else:
    return render(request, 'login_here.html')

@login_required
def logout_here(request):
  logout(request)
  return HttpResponseRedirect(reverse(('home')))


def forgot_password(request):
  if request.method == 'POST':
    form = ForgotPasswordForm(request.POST)
    if form.is_valid():
      # order = form.save(commit=False)
      # pdb.set_trace()
      password = form.cleaned_data['password']
      username = form.cleaned_data['username']
      u = User.objects.get(username=username)
      u.set_password(password)
      u.save()
      return render(request, 'login_here.html')
  else:
    form = ForgotPasswordForm()
  return render(request, 'forgot_password.html', {'form': form})

def grade_student(request):
    # pdb.set_trace()
    if request.method == 'POST':
        form = GradeStudentForm(request.POST)
        if form.is_valid():
            selected_course = form.cleaned_data['course']
            selected_assignment = form.cleaned_data['assignment']
            user = UserProfile.objects.get(user_ptr=request.user.id)
            grade = Grade.objects.get(Q(course=selected_course) & Q(assignment=selected_assignment) & Q(user=user))
        return render(request, 'grade_student.html', {'form': form, 'grade': grade})
    else:
        form = GradeStudentForm()
    return render(request, 'grade_student.html', {'form': form})

def grade_professor(request):
  if request.method == 'POST':
    form = GradeForm(request.POST)
    if form.is_valid():
      grade = form.save()
      return render(request, 'grade_success.html')
    else:
        return render(request, 'grade_nosuccess.html')
  else:
    form = GradeForm()
  return render(request, 'grade_professor.html', {'form': form})

class AboutUsView(View):

  def get(self, request):
    team_members = MembersName.objects.all()
    return render(request, 'aboutus.html', {'team_members': team_members})

def membership_detail(request, course_id):
    user = UserProfile.objects.get(user_ptr=request.user.id)
    if user.membership == 'Gold':
        video = Video.objects.all()
        return render(request, 'membership.html', {'video': video, 'user': user})
    elif user.membership == 'Silver':
        video = Video.objects.all()[:2]
        return render(request, 'membership.html', {'video': video, 'user': user})
    
def event_list(request):
    events = Events.objects.all()
    # pdb.set_trace()
    user = UserProfile.objects.get(user_ptr=request.user.id)
    if user.is_professor:
        return render(request, 'event_list.html', {'events': events})
    else:
        return render(request, 'event_list_student.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    user = UserProfile.objects.get(user_ptr=request.user.id)
    if user.is_professor:
        return render(request, 'event_detail.html', {'event': event})
    else:
        return render(request, 'event_detail_student.html', {'event': event, 'user': user})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

def event_update(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form, 'event': event})

def event_delete(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'event_confirm_delete.html', {'event': event})