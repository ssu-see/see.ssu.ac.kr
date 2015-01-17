# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(help_text=b'User name', unique=True, max_length=30)),
                ('email', models.EmailField(help_text=b'User email', unique=True, max_length=64)),
                ('contact_number', models.CharField(help_text=b'User Contact Number', max_length=30)),
                ('is_active', models.BooleanField(default=True, help_text=b'Is active user?')),
                ('is_admin', models.BooleanField(default=False, help_text=b'Is the user can access & edit admin page?')),
                ('userperm', models.CharField(default=b'1', help_text=b'Available User Permission [ User, Member, Core member, Graduate, President ]', max_length=1, choices=[(b'1', b'User'), (b'2', b'Member'), (b'3', b'Core member'), (b'4', b'Graduate'), (b'5', b'President')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
