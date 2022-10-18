from django.contrib.auth import get_user_model
from celery import shared_task
from config.celery import app

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


User = get_user_model()

def send_about_new_w(email):
    subject = "New wallpapers"
    message = 'New wallpapers are in our site'
    recipient_list = [email]
    mail.send_mail(
        subject,
        message,
        "hello@gmail.com",
        recipient_list,
    )

# В терминале: celery -A config worker -l info
@app.task
def send_all_user():
    user = User.objects.all()
    print('hello in tasks.py')
    for i in user:
        send_about_new_w(i)

# В термминале по расписанию: celery -A config beat -l info
@app.task
def send_beat_email():
    for email in User.objects.all():
        mail.send_mail("Вы подписались на рассылку",
                        "C почты сайта будет присылать вам спам для теста",
                        'hello@gmail.com',
                        [email.email])
        