# Generated by Django 4.1.4 on 2022-12-16 08:48

import api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_checklist_background_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to='backgrounds', validators=[api.validators.validate_background_image_size]),
        ),
    ]
