from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from authentication.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import (
    urlsafe_base64_decode, urlsafe_base64_encode)
from django.utils.encoding import (
    smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError)


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


def send_Password_reset_email(user_data, request):
    print("USER_ID", user_data.id)
    uidb64 = urlsafe_base64_encode(smart_bytes(user_data.id))
    token = PasswordResetTokenGenerator().make_token(user_data)
    to_mail = user_data.email
    current_site = get_current_site(request).domain
    relative_link = reverse('authentication:password-reset-confirm',
                            kwargs={'uidb64': uidb64, 'token': token})
    absurl = 'http://'+current_site+relative_link
    mail_subject = "Reset your Password"
    message = f"""
Hello {user_data.username},
You recently requested a password reset for your Freemob Account,
click the link below to reset it:
{absurl}

If you did not request a password reset, Please ignore this email
or reply to let us know. If clicking the link above doesn't work, copy
and paste it in a new browsers tab.

Thanks, Freemob Team.
    """
    email = EmailMessage(
        subject=mail_subject,
        body=message,
        to=[to_mail]

    )
    email.send()
