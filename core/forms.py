# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, MentorProfile, StudentProfile, Review, Message

class StudentRegistrationForm(UserCreationForm):
    """Form for student registration"""
    email = forms.EmailField(required=True)
    education_level = forms.ChoiceField(choices=[
        ('', 'Select your education level'),
        ('high_school', 'High School'),
        ('college', 'College'),
        ('university', 'University'),
        ('other', 'Other')
    ])
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_student = True
        
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                education_level=self.cleaned_data['education_level']
            )
        
        return user

class MentorRegistrationForm(UserCreationForm):
    """Form for mentor registration"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    expertise = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    gender = forms.ChoiceField(choices=MentorProfile.GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_mentor = True
        
        if commit:
            user.save()
            MentorProfile.objects.create(
                user=user,
                expertise=self.cleaned_data['expertise'],
                bio=self.cleaned_data['bio'],
                gender=self.cleaned_data['gender']
            )
        
        return user

class LoginForm(forms.Form):
    """Form for user login"""
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class ReviewForm(forms.ModelForm):
    """Form for submitting reviews"""
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience with this mentor...'}),
        }

class MentorFilterForm(forms.Form):
    """Form for filtering mentors"""
    expertise = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search by expertise...',
        'class': 'form-control'
    }))
    gender = forms.ChoiceField(required=False, choices=[
        ('', 'All Genders'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB', 'Non-Binary'),
        ('O', 'Other')
    ], widget=forms.Select(attrs={'class': 'form-select'}))
    min_rating = forms.ChoiceField(required=False, choices=[
        ('', 'Any Rating'),
        ('4', '4+ Stars'),
        ('3', '3+ Stars'),
        ('2', '2+ Stars'),
        ('1', '1+ Stars')
    ], widget=forms.Select(attrs={'class': 'form-select'}))



class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],  # Options: 1, 2, 3, 4, 5
        widget=forms.RadioSelect,  # No extra attrs here; we’ll style in CSS
        label='Rating'
    )
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Write your comment here...'}),
        }
        labels = {
            'comment': 'Comment',
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Type your message...'}),
        }
        labels = {
            'content': '',
        }