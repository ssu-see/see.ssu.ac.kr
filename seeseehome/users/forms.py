from django import forms
# from nocaptcha_recaptcha.fields import NoReCaptchaField
from captcha.fields import ReCaptchaField


"""
class Captcha(forms.Form):
    captcha = NoReCaptchaField()
"""


class Captcha(forms.Form):
    captcha = ReCaptchaField()
