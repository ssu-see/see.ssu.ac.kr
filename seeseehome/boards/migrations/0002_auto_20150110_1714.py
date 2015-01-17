# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachmentFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(default=b'', help_text=b"Attachment file's name", max_length=255)),
                ('md5_hash', models.CharField(default=b'', help_text=b"Attachment file's name", max_length=255, db_index=True)),
                ('timestamp', models.DateTimeField(help_text=b'Uploaded time', auto_now_add=True)),
                ('uploader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(default=b'', help_text=b'Post content'),
            preserve_default=True,
        ),
    ]
