# Generated by Django 5.1 on 2024-10-12 04:41

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_admin_comment_post_status'),
        ('register', '0003_profile_is_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_description', models.TextField()),
                ('report_count', models.IntegerField(default=0)),
                ('commented_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.profile')),
            ],
        ),
    ]
