# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('osf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='author',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='title',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='wiki',
            field=models.TextField(default=None, max_length=256, null=True),
        ),
    ]
