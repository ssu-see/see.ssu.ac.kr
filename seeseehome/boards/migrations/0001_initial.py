# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('boardname', models.CharField(default=b'', help_text=b'Board name', max_length=255)),
                ('readperm', multiselectfield.db.fields.MultiSelectField(default=[b'0', b'1', b'2', b'3', b'4', b'5'], help_text=b'Available Read Permission (It is possible to select multiple[None, User, Member, Core member, Graduate, President ]', max_length=9, choices=[(b'0', b'None'), (b'1', b'User'), (b'2', b'Member'), (b'3', b'Core member'), (b'4', b'Graduate'), (b'5', b'President')])),
                ('writeperm', multiselectfield.db.fields.MultiSelectField(default=[b'0', b'1', b'2', b'3', b'4', b'5'], help_text=b'Available Write Permission (It is possibleto select multiple[None, User, Member, Core member, Graduate, President ]', max_length=9, choices=[(b'1', b'User'), (b'2', b'Member'), (b'3', b'Core member'), (b'4', b'Graduate'), (b'5', b'President')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(help_text=b'Comment', max_length=255)),
                ('date_commented', models.DateTimeField(help_text=b'It is used to show the date commented', auto_now_add=True, db_index=True)),
                ('board', models.ForeignKey(to='boards.Board')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(default=b'', help_text=b'Post subject', max_length=255)),
                ('content', models.TextField(default=b'', help_text=b'Post content', max_length=65535)),
                ('date_posted', models.DateTimeField(help_text=b'It is used to show the date posted in admin page', auto_now_add=True, db_index=True)),
                ('is_notice', models.BooleanField(default=False, help_text=b'Is this post a notice?')),
                ('hit_count', models.IntegerField(default=0, help_text=b'counting of watched')),
                ('board', models.ForeignKey(to='boards.Board')),
                ('writer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='boards.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='writer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
