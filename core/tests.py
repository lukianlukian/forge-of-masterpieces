from django.test import TestCase, Client
from django.urls import reverse

from core.models import (
    User,
    Skill,
    FreelancerProfile,
    EmployerProfile,
    JobOffer,
    JobApplication,
    Message,
    Review,
)



def make_freelancer(username="freelancer1", password="testpass123"):
    user = User.objects.create_user(
        username=username,
        password=password,
        role=User.ROLE_FREELANCER,
    )
    profile = FreelancerProfile.objects.create(
        user=user,
        bio="Experienced developer",
        experience_level="Senior",
        years_experienced=5,
        hourly_rate=80,
        completed_projects=20,
        rating=4.5,
    )
    return user, profile


def make_employer(username="employer1", password="testpass123"):
    user = User.objects.create_user(
        username=username,
        password=password,
        role=User.ROLE_EMPLOYER,
    )
    profile = EmployerProfile.objects.create(
        user=user,
        bio="We build great products",
        company_name="Acme Corp",
    )
    return user, profile


def make_job(employer_user, title="Django Developer Needed", budget=5000):
    return JobOffer.objects.create(
        employer=employer_user,
        title=title,
        description="We need a skilled Django developer.",
        budget=budget,
        status=JobOffer.OPEN,
    )


#  Model Tests

class UserModelTest(TestCase):

    def test_is_freelancer_property(self):
        user, _ = make_freelancer()
        self.assertTrue(user.is_freelancer)
        self.assertFalse(user.is_employer)

    def test_is_employer_property(self):
        user, _ = make_employer()
        self.assertTrue(user.is_employer)
        self.assertFalse(user.is_freelancer)

    def test_str(self):
        user, _ = make_freelancer(username="john")
        self.assertEqual(str(user), "john")

    def test_default_role_is_freelancer(self):
        user = User.objects.create_user(username="newuser", password="pass1234")
        self.assertEqual(user.role, User.ROLE_FREELANCER)


class SkillModelTest(TestCase):

    def test_str(self):
        skill = Skill.objects.create(name="Python")
        self.assertEqual(str(skill), "Python")


class FreelancerProfileModelTest(TestCase):

    def test_str(self):
        user, profile = make_freelancer(username="alice")
        self.assertIn("alice", str(profile))

    def test_skills_many_to_many(self):
        _, profile = make_freelancer()
        s1 = Skill.objects.create(name="Python")
        s2 = Skill.objects.create(name="React")
        profile.skills.add(s1, s2)
        self.assertEqual(profile.skills.count(), 2)

    def test_defaults(self):
        user = User.objects.create_user(username="x", password="pass1234", role=User.ROLE_FREELANCER)
        profile = FreelancerProfile.objects.create(user=user)
        self.assertEqual(profile.completed_projects, 0)
        self.assertEqual(profile.years_experienced, 0)


class EmployerProfileModelTest(TestCase):

    def test_str(self):
        user, profile = make_employer(username="bob")
        self.assertIn("bob", str(profile))

    def test_page_views_default(self):
        _, profile = make_employer()
        self.assertEqual(profile.page_views, 0)


class JobOfferModelTest(TestCase):

    def test_str(self):
        employer, _ = make_employer()
        job = make_job(employer, title="Frontend Dev")
        self.assertEqual(str(job), "Frontend Dev")

    def test_default_status_is_open(self):
        employer, _ = make_employer()
        job = make_job(employer)
        self.assertEqual(job.status, JobOffer.OPEN)

    def test_skills_required_many_to_many(self):
        employer, _ = make_employer()
        job = make_job(employer)
        skill = Skill.objects.create(name="Vue.js")
        job.skills_required.add(skill)
        self.assertEqual(job.skills_required.count(), 1)


class JobApplicationModelTest(TestCase):

    def test_str(self):
        freelancer, _ = make_freelancer()
        employer, _ = make_employer()
        job = make_job(employer, title="API dev")
        app = JobApplication.objects.create(
            job=job,
            freelancer=freelancer,
            cover_letter="I am the best fit.",
        )
        self.assertIn(freelancer.username, str(app))
        self.assertIn(job.title, str(app))

    def test_default_status_is_pending(self):
        freelancer, _ = make_freelancer()
        employer, _ = make_employer()
        job = make_job(employer)
        app = JobApplication.objects.create(
            job=job, freelancer=freelancer, cover_letter="Hello"
        )
        self.assertEqual(app.status, JobApplication.PENDING)


class MessageModelTest(TestCase):

    def test_str(self):
        sender, _ = make_freelancer(username="sender")
        receiver, _ = make_employer(username="receiver")
        msg = Message.objects.create(sender=sender, receiver=receiver, body="Hi!")
        self.assertIn("sender", str(msg))
        self.assertIn("receiver", str(msg))

    def test_is_read_default_false(self):
        sender, _ = make_freelancer(username="s1")
        receiver, _ = make_employer(username="r1")
        msg = Message.objects.create(sender=sender, receiver=receiver, body="Hello")
        self.assertFalse(msg.is_read)


class ReviewModelTest(TestCase):

    def test_str(self):
        reviewer, _ = make_employer(username="emp_reviewer")
        reviewee, _ = make_freelancer(username="fl_reviewee")
        review = Review.objects.create(
            reviewer=reviewer,
            reviewee=reviewee,
            rating=5,
            comment="Excellent work!",
        )
        self.assertIn("5", str(review))

    def test_rating_stored_correctly(self):
        reviewer, _ = make_employer(username="emp2")
        reviewee, _ = make_freelancer(username="fl2")
        review = Review.objects.create(reviewer=reviewer, reviewee=reviewee, rating=4)
        self.assertEqual(review.rating, 4)


#  View Tests

class HomeViewTest(TestCase):

    def test_home_returns_200(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_context_counts(self):
        make_freelancer()
        make_employer()
        response = self.client.get(reverse("core:home"))
        self.assertGreaterEqual(response.context["num_freelancers"], 1)
        self.assertGreaterEqual(response.context["num_employers"], 1)


class RegisterViewTest(TestCase):

    def test_register_page_loads(self):
        response = self.client.get(reverse("core:register"))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_freelancer_profile(self):
        response = self.client.post(reverse("core:register"), {
            "username": "newfreelancer",
            "email": "f@test.com",
            "role": "freelancer",
            "password1": "ComplexPass1!",
            "password2": "ComplexPass1!",
        })
        self.assertTrue(User.objects.filter(username="newfreelancer").exists())
        user = User.objects.get(username="newfreelancer")
        self.assertTrue(hasattr(user, "freelancerprofile"))

    def test_register_creates_employer_profile(self):
        self.client.post(reverse("core:register"), {
            "username": "newemployer",
            "email": "e@test.com",
            "role": "employer",
            "password1": "ComplexPass1!",
            "password2": "ComplexPass1!",
        })
        user = User.objects.get(username="newemployer")
        self.assertTrue(hasattr(user, "employerprofile"))


class LoginViewTest(TestCase):

    def setUp(self):
        make_freelancer(username="loginuser", password="testpass123")

    def test_login_page_loads(self):
        response = self.client.get(reverse("core:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse("core:login"), {
            "username": "loginuser",
            "password": "testpass123",
        })
        self.assertRedirects(response, reverse("core:home"))

    def test_login_with_wrong_password(self):
        response = self.client.post(reverse("core:login"), {
            "username": "loginuser",
            "password": "wrongpass",
        })
        self.assertEqual(response.status_code, 200)


class LogoutViewTest(TestCase):

    def test_logout_redirects_home(self):
        make_freelancer(username="logoutuser", password="testpass123")
        self.client.login(username="logoutuser", password="testpass123")
        response = self.client.get(reverse("core:logout"))
        self.assertRedirects(response, reverse("core:home"))


class FreelancerListViewTest(TestCase):

    def test_returns_200(self):
        response = self.client.get(reverse("core:freelancer-list"))
        self.assertEqual(response.status_code, 200)

    def test_shows_freelancers(self):
        make_freelancer(username="visible_fl")
        response = self.client.get(reverse("core:freelancer-list"))
        self.assertGreaterEqual(len(response.context["freelancers"]), 1)

    def test_skill_filter(self):
        _, profile = make_freelancer(username="skill_fl")
        skill = Skill.objects.create(name="Haskell")
        profile.skills.add(skill)
        response = self.client.get(reverse("core:freelancer-list") + "?skill=Haskell")
        self.assertGreaterEqual(len(response.context["freelancers"]), 1)


class FreelancerDetailViewTest(TestCase):

    def test_returns_200(self):
        _, profile = make_freelancer()
        response = self.client.get(reverse("core:freelancer-detail", kwargs={"pk": profile.pk}))
        self.assertEqual(response.status_code, 200)

    def test_context_has_reviews(self):
        _, profile = make_freelancer()
        response = self.client.get(reverse("core:freelancer-detail", kwargs={"pk": profile.pk}))
        self.assertIn("reviews", response.context)


class EmployerDetailViewTest(TestCase):

    def test_returns_200(self):
        _, profile = make_employer()
        response = self.client.get(reverse("core:employer-detail", kwargs={"pk": profile.pk}))
        self.assertEqual(response.status_code, 200)

    def test_page_views_increments_for_non_owner(self):
        _, profile = make_employer()
        initial_views = profile.page_views
        self.client.get(reverse("core:employer-detail", kwargs={"pk": profile.pk}))
        profile.refresh_from_db()
        self.assertEqual(profile.page_views, initial_views + 1)

    def test_page_views_does_not_increment_for_owner(self):
        user, profile = make_employer(username="owner_emp")
        self.client.login(username="owner_emp", password="testpass123")
        initial_views = profile.page_views
        self.client.get(reverse("core:employer-detail", kwargs={"pk": profile.pk}))
        profile.refresh_from_db()
        self.assertEqual(profile.page_views, initial_views)


class JobListViewTest(TestCase):

    def test_returns_200(self):
        response = self.client.get(reverse("core:jobs"))
        self.assertEqual(response.status_code, 200)

    def test_shows_jobs(self):
        employer, _ = make_employer()
        make_job(employer, title="Test Job 1")
        response = self.client.get(reverse("core:jobs"))
        self.assertGreaterEqual(len(response.context["jobs"]), 1)

    def test_search_filter(self):
        employer, _ = make_employer()
        make_job(employer, title="Unique Elixir Developer")
        response = self.client.get(reverse("core:jobs") + "?q=Elixir")
        titles = [j.title for j in response.context["jobs"]]
        self.assertTrue(any("Elixir" in t for t in titles))


class JobDetailViewTest(TestCase):

    def test_returns_200(self):
        employer, _ = make_employer()
        job = make_job(employer)
        response = self.client.get(reverse("core:job-detail", kwargs={"pk": job.pk}))
        self.assertEqual(response.status_code, 200)


class JobCreateViewTest(TestCase):

    def test_employer_can_access_create_page(self):
        user, _ = make_employer(username="creator")
        self.client.login(username="creator", password="testpass123")
        response = self.client.get(reverse("core:job-create"))
        self.assertEqual(response.status_code, 200)

    def test_freelancer_cannot_access_create_page(self):
        user, _ = make_freelancer(username="cantcreate")
        self.client.login(username="cantcreate", password="testpass123")
        response = self.client.get(reverse("core:job-create"))
        self.assertEqual(response.status_code, 403)

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(reverse("core:job-create"))
        self.assertEqual(response.status_code, 302)


class JobApplyViewTest(TestCase):

    def setUp(self):
        self.employer_user, _ = make_employer(username="emp_apply")
        self.freelancer_user, _ = make_freelancer(username="fl_apply")
        self.job = make_job(self.employer_user)

    def test_freelancer_can_apply(self):
        self.client.login(username="fl_apply", password="testpass123")
        self.client.post(reverse("core:apply", kwargs={"pk": self.job.pk}), {
            "cover_letter": "I would love to work on this project.",
        })
        self.assertTrue(
            JobApplication.objects.filter(job=self.job, freelancer=self.freelancer_user).exists()
        )

    def test_cannot_apply_twice(self):
        self.client.login(username="fl_apply", password="testpass123")
        data = {"cover_letter": "First application."}
        self.client.post(reverse("core:apply", kwargs={"pk": self.job.pk}), data)
        self.client.post(reverse("core:apply", kwargs={"pk": self.job.pk}), data)
        self.assertEqual(
            JobApplication.objects.filter(job=self.job, freelancer=self.freelancer_user).count(),
            1,
        )

    def test_employer_cannot_apply(self):
        self.client.login(username="emp_apply", password="testpass123")
        self.client.post(reverse("core:apply", kwargs={"pk": self.job.pk}), {
            "cover_letter": "Trying to apply as employer.",
        })
        self.assertFalse(
            JobApplication.objects.filter(job=self.job, freelancer=self.employer_user).exists()
        )


class InboxViewTest(TestCase):

    def test_requires_login(self):
        response = self.client.get(reverse("core:inbox"))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_access(self):
        make_freelancer(username="inbox_user")
        self.client.login(username="inbox_user", password="testpass123")
        response = self.client.get(reverse("core:inbox"))
        self.assertEqual(response.status_code, 200)


class ConversationViewTest(TestCase):

    def setUp(self):
        self.fl_user, _ = make_freelancer(username="conv_fl")
        self.emp_user, _ = make_employer(username="conv_emp")

    def test_send_message(self):
        self.client.login(username="conv_fl", password="testpass123")
        self.client.post(
            reverse("core:conversation", kwargs={"user_id": self.emp_user.pk}),
            {"body": "Hello, employer!"},
        )
        self.assertTrue(
            Message.objects.filter(sender=self.fl_user, receiver=self.emp_user).exists()
        )

    def test_messages_marked_as_read(self):
        Message.objects.create(sender=self.emp_user, receiver=self.fl_user, body="Hi!", is_read=False)
        self.client.login(username="conv_fl", password="testpass123")
        self.client.get(reverse("core:conversation", kwargs={"user_id": self.emp_user.pk}))
        msg = Message.objects.get(sender=self.emp_user, receiver=self.fl_user)
        self.assertTrue(msg.is_read)


class MyApplicationsViewTest(TestCase):

    def test_requires_login(self):
        response = self.client.get(reverse("core:my-applications"))
        self.assertEqual(response.status_code, 302)
