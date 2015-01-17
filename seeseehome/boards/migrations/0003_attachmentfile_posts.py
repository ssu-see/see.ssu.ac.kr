# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20150110_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachmentfile',
            name='posts',
            field=models.ManyToManyField(to='boards.Post'),
            preserve_default=True,
        ),
    ]
