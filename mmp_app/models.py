from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Course(models.Model):
	course_name=models.CharField(max_length=256)
	file_id = models.CharField(max_length=256, default="empty")
	files = models.FileField(upload_to='Files/', blank=True, null=True)
	def __str__(self):
		return self.course_name


#class UploadFile(models.Model):

 #   courses = models.ManyToManyField(Course)


class Student(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	student_name=models.CharField(max_length=256)
	student_branch=models.CharField(max_length=256)
	courses = models.ManyToManyField(Course)

	def __str__(self):
		return self.user.username


class Faculty(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	faculty_name=models.CharField(max_length=256)
	faculty_dept=models.CharField(max_length=256)
	courses = models.ManyToManyField(Course)

	def __str__(self):
		return self.user.username
