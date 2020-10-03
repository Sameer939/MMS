from django.shortcuts import render,get_object_or_404
from mmp_app.forms import UserForm,StudentProfileInfoForm,FacultyProfileInfoForm,FileUploadForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from mmp_app.models import Course,Faculty,Student
from demo import upload
import tempfile, os
# Create your views here.

def index(request):
	return render(request,'mmp_app/index.html')


@login_required
def faculty_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

@login_required
def student_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

@login_required
def student_detail(request, Student_id):

	detail=get_object_or_404(Student,pk=Student_id)
	return render(request,'mmp_app/student_profile.html',{'Student':detail})

@login_required
def faculty_detail(request, Faculty_id):

	detail=get_object_or_404(Faculty,pk=Faculty_id)
	return render(request,'mmp_app/faculty_profile.html',{'Faculty':detail})

def faculty_register(request):
	registered=False

	if request.method=="POST":
		user_form=UserForm(data=request.POST)
		profile_form=FacultyProfileInfoForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user=user_form.save()
			user.set_password(user.password)
			user.save()

			profile=profile_form.save(commit=False)
			profile.user=user
			profile.save()
			registered=True
		else:
			print(user_form.errors,profile_form.errors)
	else:
		user_form=UserForm()
		profile_form=FacultyProfileInfoForm()

	return render(request,'mmp_app/faculty_registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def faculty_login(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')

		user=authenticate(username=username,password=password)

		if user:
			if user.is_active:
				login(request,user)
				#return HttpResponseRedirect(reverse('index'))
				faculty = Faculty.objects.filter(user = user)[0]
				context = { 'name' : faculty.faculty_name,
						'dept':faculty.faculty_dept,
						'courses':faculty.courses.all()
				}
				return render(request,'mmp_app/faculty_profile.html',context)
			else:
				return HttpResponse("Account not active")
		else:
			print('some login failed')
			print('Username: {} and password: {}'.format(username,password))
			return HttpResponse("invalid login details")
	else:
		return render(request,'mmp_app/faculty_login.html',{})

def student_register(request):
	registered=False

	if request.method=="POST":
		user_form=UserForm(data=request.POST)
		profile_form=StudentProfileInfoForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user=user_form.save()
			user.set_password(user.password)
			user.save()

			profile=profile_form.save(commit=False)
			profile.user=user
			profile.save()
			registered=True
		else:
			print(user_form.errors,profile_form.errors)
	else:
		user_form=UserForm()
		profile_form=StudentProfileInfoForm()

	return render(request,'mmp_app/student_registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def student_login(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')

		user=authenticate(username=username,password=password)

		if user:
			if user.is_active:
				login(request,user)
				#return HttpResponseRedirect(reverse('index'))
				student = Student.objects.filter(user = user)[0]
				context = { 'name' : student.student_name,
						'branch':student.student_branch,
						'courses':student.courses.all(),
				}
				return render(request,'mmp_app/student_profile.html',context)
			else:
				return HttpResponse("Account not active")
		else:
			print('some login failed')
			print('Username: {} and password: {}'.format(username,password))
			return HttpResponse("invalid login details")
	else:
		return render(request,'mmp_app/student_login.html',{})

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid():
            for f in files:
                try:
                    file_instance = Course(files=f,file_id=upload(f.name, f.file.name))
                except AttributeError:
                    filepath = None
                    with tempfile.NamedTemporaryFile("wb", delete=False) as fl:
                        filepath = fl.name
                        for chunk in f.chunks():
                            fl.write(chunk)
                    file_instance = Course(files=f,file_id=upload(f.name, filepath))
                    os.unlink(filepath)
                file_instance.save()
            return HttpResponseRedirect(reverse('index'))
        else:
        	return HttpResponse("invalid form")
    else:
        form = FileUploadForm()
        return render(request, 'mmp_app/upload_file.html',
                      {'form': form})
