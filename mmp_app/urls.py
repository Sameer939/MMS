from django.urls import path,include
from mmp_app import views

app_name='mmp_app'

urlpatterns=[
	path('faculty_login',views.faculty_login,name='faculty_login'),
    path('student_login',views.student_login,name='student_login'),
    path('faculty_register',views.faculty_register,name='faculty_register'),
    path('student_register',views.student_register,name='student_register'),
    path('upload_file',views.upload_file,name='upload_file'),
    path('student_detail',views.student_detail,name='student_detail'),
    path('faculty_detail',views.faculty_detail,name='faculty_detail'),
    path('student_logout',views.student_logout,name='student_logout'),
    path('faculty_logout',views.faculty_logout,name='faculty_logout'),
]