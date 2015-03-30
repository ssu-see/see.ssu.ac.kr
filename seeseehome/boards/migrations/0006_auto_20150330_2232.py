# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0005_auto_20150218_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='attachments',
            field=models.ManyToManyField(to='boards.AttachmentFile', blank=True),
            preserve_default=True,
        ),
    ]
