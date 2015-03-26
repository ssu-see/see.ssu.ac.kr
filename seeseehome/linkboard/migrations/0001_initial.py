# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkPost', fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)), ('description', models.CharField(
                        help_text=b'A description about the link', max_length=255)), ('url', models.URLField(
                            help_text=b'An URL for link to some information')), ('date_posted', models.DateTimeField(
                                help_text=b'It is used to show date when the link posted', auto_now_add=True, db_index=True)), ('writer', models.ForeignKey(
                                    to=settings.AUTH_USER_MODEL)), ], options={}, bases=(
                models.Model,), ), ]
