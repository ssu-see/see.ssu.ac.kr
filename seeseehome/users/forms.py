from django import forms
from captcha.fields import ReCaptchaField


class Captcha(forms.Form):
    captcha = ReCaptchaField(
        public_key='6Le72AYTAAAAADqzCojBZ6wSMTPZILFiWQXdaR6p',
    )
