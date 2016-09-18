# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20150723_2130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query',
            old_name='epidemicPrev',
            new_name='epidemic_Prevalence',
        ),
    ]
