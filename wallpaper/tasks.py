from django.contrib.auth import get_user_model
from celery import shared_task

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


User = get_user_model()


@shared_task
def send_all_user():
    user = User.objects.all()
    print('hello in tasks.py')
    for i in user:
        message = 'New wallpapers in our site'
        subject = "New wallpapers"
        recipient_list = [i]
        mail.send_mail(
            subject,
            message,
            "hello@gmail.com",
            recipient_list      
        )


# def send_about_new_w(email):
#     context = {
#         "email_text_detail": "New wallpapers in our site",
#         "email": email
#     }

#     msg_html = render_to_string("email.html", context)
#     subject = "New wallpapers"
#     plain_message = strip_tags(msg_html)
#     recipient_list = email
#     mail.send_mail(
#         subject,
#         plain_message,
#         "hello@gmail.com",
#         recipient_list,
#         html_message= msg_html
#     )