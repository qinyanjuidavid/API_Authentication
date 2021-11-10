from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from authentication.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def send_activation_mail(user_data, request):
    user = User.objects.get(email=user_data['email'])
    current_site = get_current_site(request).domain
    mail_subject = "Please Activate Your Account."
    to_mail = user.email
    token = RefreshToken.for_user(user).access_token
    relativeLink = reverse('email-verify')
    absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
    message = f"""
Welcome To FreeMob,

Hi {user.username},
Please click on the link below to confirm your email,
{absurl}
    """
    email = EmailMessage(
        subject=mail_subject,
        body=message,
        to=[to_mail]
    )
    email.send()
