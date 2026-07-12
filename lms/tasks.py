from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.timezone import now

from config.settings import EMAIL_HOST_USER
from lms.models import Course, Subscription


@shared_task
def send_email_about_update_course(course_id):
    """Отправляет письмо об обновлении курса (создании в курсе нового урока)."""

    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)
    subject = f"Обновление материалов курса {course.name}"
    message = f"В курсе {course.name} появился новый урок!"
    email_list = []
    if course.last_updated and now() - course.last_updated < timedelta(hours=4):
        return "Курс обновлялся менее 4 часов назад, письмо не отправлено"
    else:
        for sub in subscribers:
            email_list.append(sub.user.email)
            # if sub.user.tg_chat_id:                                 - для отправки сообщения в тлг
            #     send_telegram_message(sub.user.tg_chat_id, message) - еще нужно добавить поле tg_chat_id в модель User
        if email_list:
            send_mail(subject, message, EMAIL_HOST_USER, email_list)
            course.last_updated = (
                timezone.now()
            )  # для сброса начала отсчета четырех часов
            course.save()
