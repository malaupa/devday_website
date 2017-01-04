# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-04 14:55
from __future__ import unicode_literals

from django.contrib.auth.management import create_permissions
from django.db import migrations, models


def create_talk_committee(apps, schema_editor):
    for app_config in apps.get_app_configs():
        create_permissions(app_config, apps=apps, verbosity=0)

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    group, created = Group.objects.get_or_create(name='talk_committee')
    if created:
        can_vote = Permission.objects.get(content_type__app_label='talk', codename='add_vote')
        can_comment = Permission.objects.get(content_type__app_label='talk', codename='add_talkcomment')
        group.permissions.set([can_vote, can_comment])
        group.save()


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0002_alter_permission_name_max_length'),
        ('talk', '0005_auto_20170104_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='talkcomment',
            name='is_visible',
            field=models.BooleanField(default=False,
                                      help_text='Indicates whether the comment is visible to the speaker.'),
        ),
        migrations.RunPython(create_talk_committee)
    ]
