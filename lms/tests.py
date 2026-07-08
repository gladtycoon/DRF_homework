from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@email.com")
        self.course = Course.objects.create(
            name="Курс 10", description="Test Course", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Урок 1", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_create(self):
        url = reverse("lms:course-list")
        data = {"name": "Курс 20"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        data = {"name": "Курс 30"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Курс 30")

    def test_course_delete(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("lms:course-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "name": self.course.name,
                    "description": self.course.description,
                    "count_lessons_of_course": self.course.lessons.count(),
                    "all_lessons_of_course": self.course.get_lesson_names(),
                    "is_subscribed": self.course.get_is_subscribed_for_user(self.user),
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test3@email.com")
        self.course = Course.objects.create(
            name="Курс 10", description="Test Course", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Урок 1",
            description="Test Lesson",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("lms:lessons-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("lms:lessons-create")
        data = {"name": "Урок 2"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("lms:lessons-update", args=(self.lesson.pk,))
        data = {"name": "Урок 99"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Урок 99")

    def test_lesson_delete(self):
        url = reverse("lms:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lessons-list")
        response = self.client.get(url)
        data = response.json()
        print(response.json())
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "course": {
                        "id": self.course.pk,
                        "all_lessons_of_course": self.course.get_lesson_names(),
                        "name": self.course.name,
                        "preview": None,
                        "description": self.course.description,
                        "owner": self.user.pk,
                    },
                    "video_link": None,
                    "name":self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@email.com")
        self.course = Course.objects.create(name="Курс для подписки", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse("lms:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), "Подписка добавлена")
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_delete(self):
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse("lms:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), "Подписка удалена")
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_change_status(self):
        url = reverse("lms:subscription")
        data = {"course_id": self.course.pk}

        self.client.post(url, data)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        self.client.post(url, data)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
