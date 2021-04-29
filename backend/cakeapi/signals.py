# from django.dispatch import receiver

# from django.conf import settings

# from django_rest_passwordreset.signals import reset_password_token_created

# from django.core.mail import send_mail


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

#     print(reset_password_token.user.email)
#     email_plaintext_message = "copy the token====>".format(reset_password_token.key)
#     try:
#         send_mail(
#             # title:
#             "Password Reset for {title}".format(title="Some website title"),
#             # message:
#             email_plaintext_message,
#             # from:
#          '  jastestpass@gmail.com' ,
#             # to:
#             [reset_password_token.user.email]
#         )
#     except:
#         print("An exception occured .....!")