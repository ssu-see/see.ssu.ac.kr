from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField


class Captcha(forms.Form):
    captcha = NoReCaptchaField()
