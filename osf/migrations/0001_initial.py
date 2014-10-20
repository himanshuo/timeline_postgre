# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Timeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=256, blank=True)),
                ('author', models.CharField(default=b'', max_length=256, blank=True)),
                ('wiki', models.TextField(default=b'')),
                ('project_id', models.IntegerField()),
                ('date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
