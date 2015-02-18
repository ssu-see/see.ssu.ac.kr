# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_auto_20150110_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='readperm',
            field=multiselectfield.db.fields.MultiSelectField(default=[b'0', b'1', b'2', b'3', b'4', b'5'], help_text=b'Available Read Permission (It is possible to select multiple[None, User, Member, Core member, Graduate, President ]', max_length=11, choices=[(b'0', b'None'), (b'1', b'User'), (b'2', b'Member'), (b'3', b'Core member'), (b'4', b'Graduate'), (b'5', b'President')]),
            preserve_default=True,
        ),
    ]
