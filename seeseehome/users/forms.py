from django import forms
from captcha.fields import ReCaptchaField
from seeseehome.settings import settings


class Captcha(forms.Form):
    captcha = ReCaptchaField(
        public_key=settings.RECAPTCHA_SITE_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY,
        use_ssl=True
    )
