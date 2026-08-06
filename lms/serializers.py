from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_allowed_links


class CourseSerializer(ModelSerializer):
    all_lessons_of_course = SerializerMethodField()

    def get_all_lessons_of_course(self, course):
        return [lesson.name for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lessons_of_course = SerializerMethodField()
    all_lessons_of_course = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    def get_count_lessons_of_course(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_all_lessons_of_course(self, course):
        return [lesson.name for lesson in Lesson.objects.filter(course=course)]

    def get_is_subscribed(self, course):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user, course=course
            ).exists()
        return False

    class Meta:
        model = Course
        fields = (
            "name",
            "description",
            "count_lessons_of_course",
            "all_lessons_of_course",
            "is_subscribed",
        )


class LessonSerializer(ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    video_link = serializers.URLField(
        validators=[validate_allowed_links], required=False
    )

    class Meta:
        model = Lesson
        fields = "__all__"
