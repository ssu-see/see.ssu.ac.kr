# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_attachmentfile_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachmentfile',
            name='posts',
        ),
        migrations.AddField(
            model_name='post',
            name='attachments',
            field=models.ManyToManyField(to='boards.AttachmentFile'),
            preserve_default=True,
        ),
    ]
