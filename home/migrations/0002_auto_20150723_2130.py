# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query',
            old_name='query_age',
            new_name='age',
        ),
        migrations.RenameField(
            model_name='query',
            old_name='query_stage',
            new_name='stage',
        ),
        migrations.AddField(
            model_name='query',
            name='epidemicPrev',
            field=models.CharField(default=b'Low', max_length=10, choices=[(b'High', b'High'), (b'Medium', b'Medium'), (b'Low', b'Low')]),
        ),
    ]
