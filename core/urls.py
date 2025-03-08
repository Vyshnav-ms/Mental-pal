# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('faq/', views.faq_list, name='faq'),
    
    # Authentication
    path('register/', views.register_choice, name='register_choice'),  # Changed 'register' to 'register_choice' for clarity
    path('register/student/', views.register_student, name='register_student'),
    path('register/mentor/', views.register_mentor, name='register_mentor'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboards
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('mentor/dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    
    # Mentor browsing and selection
    path('mentors/', views.browse_mentors, name='browse_mentors'),
    path('mentors/<int:mentor_id>/', views.mentor_profile, name='mentor_profile'),
    path('mentors/<int:mentor_id>/select/', views.select_mentor, name='select_mentor'),
    path('mentors/<int:mentor_id>/review/', views.submit_review, name='submit_review'),
    
    # Mentorship management
    path('mentorship/<int:mentorship_id>/end/', views.end_mentorship, name='end_mentorship'),
]