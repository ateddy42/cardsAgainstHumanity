# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_played'),
    ]

    operations = [
        migrations.RenameField(
            model_name='played',
            old_name='playID',
            new_name='playerID',
        ),
    ]
