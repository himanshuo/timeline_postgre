# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('osf', '0002_auto_20141016_0414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='author',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='title',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='wiki',
            field=models.TextField(max_length=256, null=True, blank=True),
        ),
    ]
