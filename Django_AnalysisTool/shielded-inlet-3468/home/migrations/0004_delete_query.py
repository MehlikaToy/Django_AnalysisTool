# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20150723_2304'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Query',
        ),
    ]
