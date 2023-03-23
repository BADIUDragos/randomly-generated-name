from django.test import TestCase
from django.utils import timezone
from django.db.utils import IntegrityError

from polls.models import Question


class TestQuestion(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.question1 = Question.objects.create(question_text="What's your name ?", pub_date=timezone.now())

    def test_question_text_is_unique(self):
        with self.assertRaisesMessage(IntegrityError, "UNIQUE constraint failed: polls_question.question_text"):
            question2 = Question.objects.create(question_text="What's your name ?", pub_date=timezone.now())

    def test_create_question_different_text(self):
        self.assertEqual(Question.objects.all().count(), 1)

        question2 = Question.objects.create(question_text="How are you ?", pub_date=timezone.now())

        self.assertEqual(Question.objects.all().count(), 2)


class TestChoice(TestCase):

    question1 = None

    @classmethod
    def setUpTestData(cls):
        cls.question1 = Question.objects.create(question_text="What's your name ?", pub_date=timezone.now())
        cls.question1.choice_set.create(choice_text='Looking for a new job', votes=0)

    def test_unique_choices_in_question(self):
        with self.assertRaisesMessage(IntegrityError,  'UNIQUE constraint failed: polls_choice.question_id, '
                                                       'polls_choice.choice_text'):
            self.question1.choice_set.create(choice_text='Looking for a new job', votes=0)

    def test_different_question_same_choice(self):
        question2 = Question.objects.create(question_text="How are you ?", pub_date=timezone.now())
        question2.choice_set.create(choice_text='Looking for a new job', votes=0)

        self.assertEqual(str(self.question1.choice_set.all()), str(question2.choice_set.all()))
