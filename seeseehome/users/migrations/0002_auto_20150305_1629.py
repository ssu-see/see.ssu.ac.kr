# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='signup_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='userperm',
            field=models.CharField(default=b'1', help_text=b'Available User Permission         [ User, Member, Core member, Graduate, President ]', max_length=1, choices=[(b'1', b'User'), (b'2', b'Member'), (b'3', b'Core member'), (b'4', b'Graduate'), (b'5', b'President')]),
            preserve_default=True,
        ),
    ]
