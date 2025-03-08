# core/admin.py

from django.contrib import admin
from .models import User, MentorProfile, StudentProfile, Mentorship, FAQ, Review

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_student', 'is_mentor', 'verified')
    list_filter = ('is_student', 'is_mentor', 'verified')
    search_fields = ('username', 'email')

@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'gender')
    list_filter = ('gender',)
    search_fields = ('user__username', 'expertise', 'bio')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'education_level')
    list_filter = ('education_level',)
    search_fields = ('user__username',)

@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):
    list_display = ('student', 'mentor', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('student__username', 'mentor__username')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')
    list_filter = ('category',)
    search_fields = ('question', 'answer', 'category')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'mentor', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('student__username', 'mentor__username', 'comment')