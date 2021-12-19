from django.http import response
from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone
import datetime
from .models import Question

def create_question(question_text, days):
    """Creates a polls Question with given question_text and publication date.
    The days is an offset to django.timezone.now(), negative or possitive.
    """
    now = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=now)

class QuestionModelTestCase(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose
        pub_date is in the future
        """
        _time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=_time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        """returns_publised_recently() returns False for questions whose
        pub_date is older than 1 day """
        now = timezone.now()
        old_question = Question(pub_date=now - datetime.timedelta(days=1,
            seconds=1))
        self.assertFalse(old_question.was_published_recently())
        

    def test_was_published_recently_with_recent_question(self):
        """was_publised_recently() return True for question whose pub_date
        is not older than 1 day"""
        now = timezone.now()
        recent_question = Question(pub_date=now - datetime.timedelta(hours=23,
            minutes=59, seconds=59))
        self.assertTrue(recent_question.was_published_recently())

class QuestionIndexViewTestCase(TestCase):
    def test_no_question(self):
        """If no questions exist, an appropriate message is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_questions"], [])
    
    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page
        """
        question = create_question("past question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_questions"],
            [question])
    
    def test_future_question(self):
        """Questions with pub_date in the future shouldn't be displayed on the
        index page
        """
        question = create_question("future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_questions"], [])
    
    def test_future_question_and_past_question(self):
        """Questions with pub_date in the past should only be displayed
        """
        past_question = create_question("past question", days=-30)
        future_question = create_question("future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_questions"],
            [past_question])

    def test_two_past_questions(self):
        """The index page should display more than one questions
        """
        past_question1 = create_question("past question 1", days=-30)
        past_question2 = create_question("past question 2", days=-20)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_questions"],
            [past_question2, past_question1])

class QuestionDetailViewTestCase(TestCase):
    def test_future_question(self):
        """Future questions shouldn't be displayed on detail view
        """
        future_question = create_question("future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """past questions should be displayed on the detail view
        """
        past_question = create_question("past question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
