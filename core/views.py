from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.http import HttpResponseForbidden

from .models import User, MentorProfile, StudentProfile, Mentorship, FAQ, Review, Message
from .forms import (
    StudentRegistrationForm, MentorRegistrationForm, LoginForm, 
    ReviewForm, MentorFilterForm, MessageForm
)

def home(request):
    """Home page view"""
    return render(request, 'core/home.html')

def register_choice(request):
    """View to choose registration type (student or mentor)"""
    return render(request, 'core/register_choice.html')

def register_student(request):
    """Student registration view"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True  # Set as student
            user.save()
            
            # Create student profile (assuming StudentProfile exists in models)
            # Note: StudentProfile isn't in your provided models.py, so adjust if needed
            # If StudentProfile doesn't exist, remove this block
            StudentProfile.objects.create(
                user=user,
                education_level=form.cleaned_data['education_level']
            )
            
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'core/register_student.html', {'form': form})

def register_mentor(request):
    """Mentor registration view"""
    if request.method == 'POST':
        form = MentorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This calls the custom save method
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
            print("Form errors:", form.errors)  # Debug output to terminal
    else:
        form = MentorRegistrationForm()
    return render(request, 'core/register_mentor.html', {'form': form})

def user_login(request):
    """Login view for both students and mentors"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                if user.is_student:
                    return redirect('student_dashboard')
                elif user.is_mentor:
                    return redirect('mentor_dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'core/login.html', {'form': form})

def user_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def student_dashboard(request):
    """Dashboard for students"""
    if not request.user.is_student:
        return HttpResponseForbidden("Access denied. Student account required.")
    
    # Get student's mentorships
    mentorships = Mentorship.objects.filter(student=request.user, active=True)
    
    # Get recommended mentors (simple random selection)
    recommended_mentors = MentorProfile.objects.exclude(
        user__in=mentorships.values_list('mentor', flat=True)
    ).order_by('?')[:3]  # Random selection for simplicity
    
    context = {
        'mentorships': mentorships,
        'recommended_mentors': recommended_mentors,
    }
    
    return render(request, 'core/student_dashboard.html', context)

@login_required
def mentor_dashboard(request):
    """View for mentor dashboard"""
    if not request.user.is_mentor:
        messages.error(request, 'Only mentors can access this page.')
        return redirect('home')
    
    # Get active mentorships
    mentorships = Mentorship.objects.filter(mentor=request.user, active=True)
    
    # Get reviews for the mentor
    reviews = Review.objects.filter(mentor=request.user)
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] if reviews.exists() else None
    
    context = {
        'mentorships': mentorships,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'core/mentor_dashboard.html', context)

@login_required
def browse_mentors(request):
    """View for browsing and filtering mentors"""
    if not request.user.is_student:
        messages.error(request, 'Only students can browse mentors.')
        return redirect('home')
    
    form = MentorFilterForm(request.GET)
    mentors = MentorProfile.objects.all()  # No verification check
    
    # Apply filters if form is valid
    if form.is_valid():
        expertise = form.cleaned_data.get('expertise')
        gender = form.cleaned_data.get('gender')
        min_rating = form.cleaned_data.get('min_rating')
        
        if expertise:
            mentors = mentors.filter(expertise__icontains=expertise)
        
        if gender:
            mentors = mentors.filter(gender=gender)
        
        if min_rating:
            mentors_with_min_rating = [
                mentor.id for mentor in mentors 
                if mentor.average_rating() >= float(min_rating)
            ]
            mentors = mentors.filter(id__in=mentors_with_min_rating)
    
    context = {
        'form': form,
        'mentors': mentors,
    }
    
    return render(request, 'core/browse_mentors.html', context)

@login_required
def mentor_profile(request, mentor_id):
    """View for mentor profile details"""
    mentor = get_object_or_404(User, id=mentor_id, is_mentor=True)
    mentor_profile = mentor.mentor_profile
    reviews = Review.objects.filter(mentor=mentor).order_by('-created_at')
    
    # Check if the student has a mentorship with this mentor
    has_mentorship = False
    if request.user.is_student:
        has_mentorship = Mentorship.objects.filter(
            student=request.user, 
            mentor=mentor,
            active=True
        ).exists()
    
    # Check if the student has already reviewed this mentor
    has_reviewed = False
    if request.user.is_student:
        has_reviewed = Review.objects.filter(
            student=request.user,
            mentor=mentor
        ).exists()
    
    context = {
        'mentor': mentor,
        'mentor_profile': mentor_profile,
        'reviews': reviews,
        'has_mentorship': has_mentorship,
        'has_reviewed': has_reviewed,
    }
    
    return render(request, 'core/mentor_profile.html', context)

@login_required
def select_mentor(request, mentor_id):
    """View for selecting a mentor"""
    if not request.user.is_student:
        messages.error(request, 'Only students can select mentors.')
        return redirect('home')
    mentor = get_object_or_404(User, id=mentor_id, is_mentor=True)
    
    # Check for any existing mentorship (active or inactive)
    mentorship = Mentorship.objects.filter(student=request.user, mentor=mentor).first()
    
    if mentorship:
        if mentorship.active:
            messages.info(request, f'You are already connected with {mentor.username}.')
        else:
            # Reactivate the existing mentorship
            mentorship.active = True
            mentorship.save()
            messages.success(request, f'You have reconnected with {mentor.username}!')
    else:
        # Create a new mentorship if none exists
        Mentorship.objects.create(student=request.user, mentor=mentor)
        messages.success(request, f'You are now connected with {mentor.username}!')
    
    return redirect('student_dashboard')
@login_required
def end_mentorship(request, mentorship_id):
    """View for ending a mentorship"""
    mentorship = get_object_or_404(Mentorship, id=mentorship_id)
    
    # Ensure the user is authorized to end this mentorship
    if request.user != mentorship.student and request.user != mentorship.mentor:
        return HttpResponseForbidden("You don't have permission to end this mentorship.")
    
    mentorship.active = False
    mentorship.save()
    
    messages.success(request, 'The mentorship has been ended.')
    
    if request.user.is_student:
        return redirect('student_dashboard')
    else:
        return redirect('mentor_dashboard')

@login_required
def submit_review(request, mentor_id):
    """View for submitting a review for a mentor"""
    if not request.user.is_student:
        messages.error(request, 'Only students can submit reviews.')
        return redirect('home')
    
    mentor = get_object_or_404(User, id=mentor_id, is_mentor=True)
    
    # Check if student has a mentorship with this mentor
    has_mentorship = Mentorship.objects.filter(
        student=request.user, 
        mentor=mentor
    ).exists()
    
    if not has_mentorship:
        messages.error(request, 'You can only review mentors you have worked with.')
        return redirect('browse_mentors')
    
    # Check if student has already reviewed this mentor
    existing_review = Review.objects.filter(
        student=request.user,
        mentor=mentor
    ).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            if not existing_review:
                review.student = request.user
                review.mentor = mentor
            review.save()
            
            messages.success(request, 'Your review has been submitted!')
            return redirect('mentor_profile', mentor_id=mentor.id)
    else:
        form = ReviewForm(instance=existing_review)
    
    context = {
        'form': form,
        'mentor': mentor,
        'is_edit': existing_review is not None
    }
    
    return render(request, 'core/submit_review.html', context)

def faq_list(request):
    """View for FAQ page"""
    faqs = FAQ.objects.all().order_by('category', 'id')
    
    # Group FAQs by category
    categories = {}
    for faq in faqs:
        if faq.category not in categories:
            categories[faq.category] = []
        categories[faq.category].append(faq)
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'core/faq.html', context)



#submit review
@login_required
def submit_review(request, mentor_id):
    """View for submitting a review for a mentor"""
    if not request.user.is_student:
        messages.error(request, 'Only students can submit reviews.')
        return redirect('home')
    mentor = get_object_or_404(User, id=mentor_id, is_mentor=True)
    has_mentorship = Mentorship.objects.filter(
        student=request.user, 
        mentor=mentor
    ).exists()
    if not has_mentorship:
        messages.error(request, 'You can only review mentors you have worked with.')
        return redirect('browse_mentors')
    existing_review = Review.objects.filter(
        student=request.user,
        mentor=mentor
    ).first()
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            if not existing_review:
                review.student = request.user
                review.mentor = mentor
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('mentor_profile', mentor_id=mentor.id)
    else:
        form = ReviewForm(instance=existing_review)
    context = {
        'form': form,
        'mentor': mentor,
        'is_edit': existing_review is not None
    }
    return render(request, 'core/submit_review.html', context)



@login_required
def inbox(request):
    """View for displaying the user's inbox"""
    if request.user.is_student:
        mentorships = Mentorship.objects.filter(student=request.user, active=True)
        other_role = 'mentor'
    elif request.user.is_mentor:
        mentorships = Mentorship.objects.filter(mentor=request.user, active=True)
        other_role = 'student'
    else:
        return redirect('home')
    
    conversations = []
    for mentorship in mentorships:
        unread_count = Message.objects.filter(
            mentorship=mentorship,
            receiver=request.user,
            is_read=False
        ).count()
        last_message = Message.objects.filter(mentorship=mentorship).order_by('-timestamp').first()
        conversations.append({
            'mentorship': mentorship,
            'other_user': getattr(mentorship, other_role),
            'unread_count': unread_count,
            'last_message': last_message,
        })
    
    context = {
        'conversations': conversations,
    }
    return render(request, 'core/inbox.html', context)

@login_required
def chat(request, mentorship_id):
    """View for chatting within a mentorship"""
    mentorship = get_object_or_404(Mentorship, id=mentorship_id, active=True)
    
    # Check if user is part of this mentorship
    if request.user != mentorship.student and request.user != mentorship.mentor:
        return HttpResponseForbidden("You don't have permission to access this chat.")
    
    # Mark messages as read
    Message.objects.filter(
        mentorship=mentorship,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)
    
    # Get all messages (renamed to avoid conflict)
    chat_messages = Message.objects.filter(mentorship=mentorship).order_by('timestamp')
    
    # Handle form submission
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.mentorship = mentorship
            message.sender = request.user
            message.receiver = mentorship.mentor if request.user.is_student else mentorship.student
            message.save()
            
            messages.success(request, 'Message sent!')  # Use Django's messages framework
            form = MessageForm()  # Clear the form after submission
    else:
        form = MessageForm()
    
    context = {
        'mentorship': mentorship,
        'messages': chat_messages,  # Updated name
        'form': form,
        'other_user': mentorship.mentor if request.user.is_student else mentorship.student,
    }
    return render(request, 'core/chat.html', context)