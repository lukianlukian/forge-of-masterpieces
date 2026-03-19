import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from core.models import (
    Skill,
    FreelancerProfile,
    EmployerProfile,
    JobOffer,
    JobApplication,
    Message,
    Review,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Fill database with test data for WorkForge"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Deleting old test data..."))

        Review.objects.all().delete()
        Message.objects.all().delete()
        JobApplication.objects.all().delete()
        JobOffer.objects.all().delete()
        FreelancerProfile.objects.all().delete()
        EmployerProfile.objects.all().delete()
        Skill.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write(self.style.SUCCESS("Old data deleted."))

        # ----------------------------
        # Skills
        # ----------------------------
        skill_names = [
            "Python",
            "Django",
            "JavaScript",
            "React",
            "HTML",
            "CSS",
            "PostgreSQL",
            "SQL",
            "UI/UX",
            "Figma",
            "REST API",
            "Git",
            "Docker",
            "Bootstrap",
            "Tailwind",
            "Data Analysis",
        ]

        skills = [Skill.objects.create(name=name) for name in skill_names]
        self.stdout.write(self.style.SUCCESS(f"Created {len(skills)} skills."))

        # ----------------------------
        # Employers
        # ----------------------------
        employer_data = [
            {
                "username": "techcorp",
                "email": "techcorp@example.com",
                "first_name": "Tech",
                "last_name": "Corp",
                "company_name": "TechCorp Ltd",
                "bio": "We build internal business tools and scalable web apps.",
                "avatar": "avatars/employer1.jpg",
            },
            {
                "username": "designhub",
                "email": "designhub@example.com",
                "first_name": "Design",
                "last_name": "Hub",
                "company_name": "DesignHub Studio",
                "bio": "Creative agency focused on product design and branding.",
                "avatar": "avatars/employer3.jpg",
            },
            {
                "username": "startupx",
                "email": "startupx@example.com",
                "first_name": "Startup",
                "last_name": "X",
                "company_name": "StartupX",
                "bio": "Fast-growing startup looking for talented freelancers.",
                "avatar": "avatars/employer3.jpg",
            },
        ]

        employers = []

        for data in employer_data:
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password="12345678",
                first_name=data["first_name"],
                last_name=data["last_name"],
                role=User.ROLE_EMPLOYER,
                avatar=data["avatar"],
            )

            EmployerProfile.objects.create(
                user=user,
                bio=data["bio"],
                company_name=data["company_name"],
                page_views=random.randint(20, 500),
            )

            employers.append(user)

        self.stdout.write(self.style.SUCCESS(f"Created {len(employers)} employers."))

        # ----------------------------
        # Freelancers
        # ----------------------------
        freelancer_data = [
            {
                "username": "alexdev",
                "email": "alex@example.com",
                "first_name": "Alex",
                "last_name": "Johnson",
                "bio": "Backend developer with strong Django experience.",
                "experience_level": "senior",
                "years_experienced": 6,
                "hourly_rate": Decimal("45.00"),
                "completed_projects": 22,
                "rating": Decimal("4.80"),
                "avatar": "avatars/freelancer1.jpg",
            },
            {
                "username": "mariadesign",
                "email": "maria@example.com",
                "first_name": "Maria",
                "last_name": "Lopez",
                "bio": "UI/UX designer focused on clean interfaces.",
                "experience_level": "middle",
                "years_experienced": 4,
                "hourly_rate": Decimal("35.00"),
                "completed_projects": 18,
                "rating": Decimal("4.60"),
                "avatar": "avatars/freelancer2.jpg",
            },
            {
                "username": "johnreact",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Carter",
                "bio": "Frontend developer specializing in React and Tailwind.",
                "experience_level": "middle",
                "years_experienced": 3,
                "hourly_rate": Decimal("32.00"),
                "completed_projects": 14,
                "rating": Decimal("4.40"),
                "avatar": "avatars/freelancer3.jpg",
            },
            {
                "username": "sofiadata",
                "email": "sofia@example.com",
                "first_name": "Sofia",
                "last_name": "Brown",
                "bio": "Data analyst who loves dashboards and SQL.",
                "experience_level": "junior",
                "years_experienced": 2,
                "hourly_rate": Decimal("25.00"),
                "completed_projects": 9,
                "rating": Decimal("4.20"),
                "avatar": "avatars/freelancer4.jpg",
            },
            {
                "username": "maxfullstack",
                "email": "max@example.com",
                "first_name": "Max",
                "last_name": "Taylor",
                "bio": "Full-stack freelancer working with Django and JS.",
                "experience_level": "senior",
                "years_experienced": 7,
                "hourly_rate": Decimal("50.00"),
                "completed_projects": 30,
                "rating": Decimal("4.95"),
                "avatar": "avatars/freelancer5.jpg",
            },
        ]

        freelancers = []

        for data in freelancer_data:
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password="12345678",
                first_name=data["first_name"],
                last_name=data["last_name"],
                role=User.ROLE_FREELANCER,
                avatar=data["avatar"],
            )

            profile = FreelancerProfile.objects.create(
                user=user,
                bio=data["bio"],
                experience_level=data["experience_level"],
                years_experienced=data["years_experienced"],
                hourly_rate=data["hourly_rate"],
                completed_projects=data["completed_projects"],
                rating=data["rating"],
            )

            assigned_skills = random.sample(skills, random.randint(3, 6))
            profile.skills.set(assigned_skills)

            freelancers.append(user)

        self.stdout.write(self.style.SUCCESS(f"Created {len(freelancers)} freelancers."))

        # ----------------------------
        # Job Offers
        # ----------------------------
        job_data = [
            {
                "employer": employers[0],
                "title": "Django Backend Developer Needed",
                "description": "Looking for a Django developer to build APIs and admin dashboard.",
                "budget": Decimal("1200.00"),
                "status": JobOffer.OPEN,
                "skills": ["Python", "Django", "REST API", "PostgreSQL"],
            },
            {
                "employer": employers[1],
                "title": "UI/UX Designer for SaaS Dashboard",
                "description": "Need a designer to improve dashboard flow and visual hierarchy.",
                "budget": Decimal("800.00"),
                "status": JobOffer.OPEN,
                "skills": ["UI/UX", "Figma"],
            },
            {
                "employer": employers[2],
                "title": "React Frontend Developer",
                "description": "Need a freelancer to build responsive pages with React.",
                "budget": Decimal("950.00"),
                "status": JobOffer.OPEN,
                "skills": ["JavaScript", "React", "HTML", "CSS", "Tailwind"],
            },
            {
                "employer": employers[0],
                "title": "Full-stack Platform Improvements",
                "description": "Upgrade an internal platform with Django + JavaScript.",
                "budget": Decimal("1500.00"),
                "status": JobOffer.CLOSED,
                "skills": ["Python", "Django", "JavaScript", "SQL"],
            },
            {
                "employer": employers[1],
                "title": "Data Analyst for Reporting",
                "description": "Build reports from platform usage data and present insights.",
                "budget": Decimal("700.00"),
                "status": JobOffer.OPEN,
                "skills": ["Data Analysis", "SQL", "PostgreSQL"],
            },
        ]

        jobs = []

        for item in job_data:
            job = JobOffer.objects.create(
                employer=item["employer"],
                title=item["title"],
                description=item["description"],
                budget=item["budget"],
                status=item["status"],
            )
            needed_skills = Skill.objects.filter(name__in=item["skills"])
            job.skills_required.set(needed_skills)
            jobs.append(job)

        self.stdout.write(self.style.SUCCESS(f"Created {len(jobs)} job offers."))

        # ----------------------------
        # Job Applications
        # ----------------------------
        application_templates = [
            "Hello, I have relevant experience and would love to help with this project.",
            "I am interested in this opportunity and can start immediately.",
            "This job matches my skills very well. I would be happy to discuss details.",
            "I have done similar work before and can deliver quality results.",
            "I believe I am a strong fit for this project and would like to apply.",
        ]

        applications = []

        for job in jobs:
            chosen_freelancers = random.sample(
                freelancers,
                random.randint(2, min(4, len(freelancers)))
            )
            for freelancer in chosen_freelancers:
                app = JobApplication.objects.create(
                    job=job,
                    freelancer=freelancer,
                    cover_letter=random.choice(application_templates),
                    status=random.choice([
                        JobApplication.PENDING,
                        JobApplication.PENDING,
                        JobApplication.ACCEPTED,
                        JobApplication.REJECTED,
                    ]),
                )
                applications.append(app)

        self.stdout.write(self.style.SUCCESS(f"Created {len(applications)} applications."))

        # ----------------------------
        # Messages
        # ----------------------------
        message_texts = [
            "Hi! I reviewed your profile and would like to discuss the project.",
            "Thanks for applying. Are you available this week?",
            "Yes, I am available. Could you share more project details?",
            "Your proposal looks good. What is your expected timeline?",
            "I can finish the first version in 5 days.",
            "Great, let's continue in chat and discuss milestones.",
        ]

        messages_created = 0

        for _ in range(20):
            employer = random.choice(employers)
            freelancer = random.choice(freelancers)

            Message.objects.create(
                sender=employer,
                receiver=freelancer,
                body=random.choice(message_texts),
                is_read=random.choice([True, False]),
            )
            messages_created += 1

            Message.objects.create(
                sender=freelancer,
                receiver=employer,
                body=random.choice(message_texts),
                is_read=random.choice([True, False]),
            )
            messages_created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {messages_created} messages."))

        # ----------------------------
        # Reviews
        # ----------------------------
        reviews_created = 0

        for _ in range(12):
            reviewer = random.choice(employers)
            reviewee = random.choice(freelancers)

            Review.objects.create(
                reviewer=reviewer,
                reviewee=reviewee,
                rating=random.randint(3, 5),
                comment=random.choice([
                    "Good communication and quality work.",
                    "Delivered on time and met expectations.",
                    "Professional freelancer, would hire again.",
                    "Solid work, smooth collaboration.",
                    "Very reliable and responsive.",
                ]),
            )
            reviews_created += 1

        for _ in range(5):
            reviewer = random.choice(freelancers)
            reviewee = random.choice(employers)

            Review.objects.create(
                reviewer=reviewer,
                reviewee=reviewee,
                rating=random.randint(3, 5),
                comment=random.choice([
                    "Clear requirements and fast feedback.",
                    "Pleasant client to work with.",
                    "Professional communication throughout the project.",
                    "Project was well organized.",
                ]),
            )
            reviews_created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {reviews_created} reviews."))
        self.stdout.write(self.style.SUCCESS("Database successfully seeded!"))
        self.stdout.write(self.style.WARNING("Test password for all users: 12345678"))