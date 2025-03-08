# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    """Custom user model with student/mentor roles"""
    is_student = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.username

class MentorProfile(models.Model):
    """Profile for mentors with additional information"""
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB', 'Non-Binary'),
        ('O', 'Other'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    expertise = models.CharField(max_length=100)
    bio = models.TextField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    
    def __str__(self):
        return f"{self.user.username}'s Mentor Profile"
    
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = Review.objects.filter(mentor=self.user)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return 0
    
    def review_count(self):
        """Count number of reviews"""
        return Review.objects.filter(mentor=self.user).count()

class StudentProfile(models.Model):
    """Profile for students with additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    education_level = models.CharField(max_length=50, blank=True)  # e.g., "High School", "College"
    
    def __str__(self):
        return f"{self.user.username}'s Student Profile"

class Mentorship(models.Model):
    """Tracks student-mentor relationships"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_mentorships')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_mentorships')
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.mentor.username}"
    
    class Meta:
        unique_together = ('student', 'mentor')

class FAQ(models.Model):
    """Frequently asked questions"""
    category = models.CharField(max_length=100)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    
    def __str__(self):
        return self.question

class Review(models.Model):
    """Reviews from students for mentors"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.student.username} for {self.mentor.username}"
    
    class Meta:
        unique_together = ('student', 'mentor')