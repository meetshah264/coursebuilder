from django.db import models
from django.contrib.auth.models import User
from django.core import validators

class UserProfile(User):
  fullname = models.CharField(max_length=30, null=True)
  is_student = models.BooleanField(default=True)
  is_professor = models.BooleanField(default=False)
  MEMBERSHIP_CHOICES = [
    ('Bronze', 'Bronze'),
    ('Silver', 'Silver'),
    ('Gold', 'Gold'),
  ]
  membership = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, default='B')
  
  def __str__(self):
    return self.fullname

class Course(models.Model):
  user = models.ManyToManyField(UserProfile)
  title = models.CharField(max_length=200)
  description = models.TextField()
  price = models.FloatField( null=True, blank=True,
        verbose_name='Price',
        validators=[
            validators.MinValueValidator(50),
            validators.MaxValueValidator(100000)
        ]
  )

  def __str__(self):
    return self.title

class Assignment(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  description = models.TextField()
  due_date = models.DateField()
  file = models.FileField(upload_to='assignments/')
  def __str__(self):
    return self.title

class Grade(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
  grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

  def __str__(self):
    return str(self.grade)
  
class Labs(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  description = models.TextField()
  lab_date = models.DateField()
  file = models.FileField(upload_to='labs/')

  def __str__(self):
    return self.title

class Notes(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  content = models.TextField()

  def __str__(self):
    return self.title

class PPT(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  file = models.FileField(upload_to='ppt_files/')

  def __str__(self):
    return self.title

class CourseEvent(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  description = models.TextField()
  start = models.DateTimeField()
  end = models.DateTimeField()

  def __str__(self):
    return self.title

class MembersName(models.Model):
  first_name = models.CharField(max_length=50, null=False)
  last_name = models.CharField(max_length=50, null=False)
  # semester = models.PositiveIntegerField(default=3)
  # link = models.URLField()

  def __str__(self):
    return self.first_name

class Events(models.Model):
  user = models.ManyToManyField(UserProfile)
  title = models.CharField(max_length=200)
  description = models.TextField()
  price = models.FloatField( null=True, blank=True,
        verbose_name='Price',
        validators=[
            validators.MinValueValidator(50),
            validators.MaxValueValidator(100000)
        ]
  )

  def __str__(self):
    return self.title

class Video(models.Model):
  title = models.CharField(max_length=200)
  video_file = models.FileField(upload_to='videos/%y')
  description = models.TextField()

  def __str__(self):
    return self.title