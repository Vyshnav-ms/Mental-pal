# core/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import FAQ, MentorProfile, User

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create FAQs
        self.create_faqs()
        
        # Create sample mentors (for development)
        if not User.objects.filter(is_mentor=True).exists():
            self.create_sample_mentors()
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
    
    def create_faqs(self):
        """Create initial FAQs"""
        faqs_data = [
            {
                'category': 'Getting Started',
                'question': 'How do I sign up for MentalPal?',
                'answer': 'Signing up for MentalPal is easy! Click the "Sign Up" button in the top right corner of the homepage. You\'ll need to provide a valid email address, create a username and password, and select your role (student). After submitting the form, you\'ll receive a verification email with a link to activate your account.'
            },
            {
                'category': 'Getting Started',
                'question': 'Is MentalPal completely anonymous?',
                'answer': 'MentalPal provides a confidential environment where your personal information is protected. While mentors will know your username, you can choose how much personal information to share. All conversations between you and your mentor are private and secure.'
            },
            {
                'category': 'Mentorship',
                'question': 'How do I choose a mentor?',
                'answer': 'You can browse our list of verified mentors by visiting the "Find Mentors" page. You can filter mentors by expertise, gender, and other criteria. Each mentor profile includes their bio, expertise, and reviews from other students. Once you find a mentor who seems like a good fit, you can click "Connect" to establish a mentorship relationship.'
            },
            {
                'category': 'Mentorship',
                'question': 'Can I change my mentor if we\'re not a good fit?',
                'answer': 'Yes, you can change your mentor at any time. We understand that finding the right mentor is important for your mental health journey. If you feel your current mentor isn\'t the right fit, you can end the mentorship and select a new mentor without any penalties.'
            },
            {
                'category': 'Support',
                'question': 'What kind of support can I expect from my mentor?',
                'answer': 'Mentors provide personalized guidance, resources, and support for your mental health concerns. They can help you develop coping strategies, provide a listening ear, and offer perspective on challenges you\'re facing. However, please note that MentalPal is not a crisis service or a replacement for professional therapy when needed.'
            },
            {
                'category': 'Support',
                'question': 'What should I do in a mental health emergency?',
                'answer': 'MentalPal is not designed for crisis intervention. If you\'re experiencing a mental health emergency, please contact your local emergency services (911 in the US), call the National Suicide Prevention Lifeline at 1-800-273-8255, or text HOME to 741741 to reach the Crisis Text Line. Your mentor can provide follow-up support after the immediate crisis has been addressed by appropriate emergency services.'
            },
            {
                'category': 'Privacy & Security',
                'question': 'How is my personal information protected?',
                'answer': 'MentalPal takes your privacy seriously. We use industry-standard encryption to protect your data and conversations. We never share your personal information with third parties without your consent. You can review our complete Privacy Policy for more details on how we collect, use, and protect your information.'
            },
            {
                'category': 'Privacy & Security',
                'question': 'Can my school or parents see my conversations with my mentor?',
                'answer': 'No. Your conversations with your mentor are private and confidential. Neither your school nor your parents have access to these conversations. The only exception would be if there is a legal requirement to disclose information, such as if there is an immediate risk of harm to yourself or others.'
            }
        ]
        
        # Delete existing FAQs if any
        FAQ.objects.all().delete()
        
        # Create new FAQs
        for faq_data in faqs_data:
            FAQ.objects.create(**faq_data)
        
        self.stdout.write(f'Created {len(faqs_data)} FAQs')
    
    def create_sample_mentors(self):
        """Create sample mentors for development"""
        User = get_user_model()
        
        mentors_data = [
            {
                'username': 'dr_sarah',
                'email': 'sarah@example.com',
                'password': 'password123',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'profile': {
                    'expertise': 'Anxiety & Depression',
                    'bio': 'Clinical psychologist with 10+ years of experience helping students navigate anxiety and depression.',
                    'gender': 'F'
                }
            },
            {
                'username': 'michael_chen',
                'email': 'michael@example.com',
                'password': 'password123',
                'first_name': 'Michael',
                'last_name': 'Chen',
                'profile': {
                    'expertise': 'Academic Stress',
                    'bio': 'Licensed therapist specializing in helping students manage academic pressure and build healthy coping mechanisms.',
                    'gender': 'M'
                }
            },
            {
                'username': 'dr_patel',
                'email': 'aisha@example.com',
                'password': 'password123',
                'first_name': 'Aisha',
                'last_name': 'Patel',
                'profile': {
                    'expertise': 'Self-Esteem & Identity',
                    'bio': 'Counselor focused on helping students develop positive self-image and navigate identity challenges.',
                    'gender': 'F'
                }
            }
        ]
        
        for mentor_data in mentors_data:
            profile_data = mentor_data.pop('profile')
            
            # Create user
            user = User.objects.create_user(
                **mentor_data,
                is_mentor=True,
                verified=True  # Pre-verified for development
            )
            
            # Create mentor profile
            MentorProfile.objects.create(
                user=user,
                **profile_data
            )
        
        self.stdout.write(f'Created {len(mentors_data)} sample mentors')