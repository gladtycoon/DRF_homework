from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


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

    def get_count_lessons_of_course(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_all_lessons_of_course(self, course):
        return [lesson.name for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = (
            "name",
            "description",
            "count_lessons_of_course",
            "all_lessons_of_course",
        )


class LessonSerializer(ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Lesson
        fields = "__all__"
