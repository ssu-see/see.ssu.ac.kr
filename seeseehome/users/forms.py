from django import forms
from captcha.fields import ReCaptchaField


class Captcha(forms.Form):
    captcha = ReCaptchaField()
