# Generated by Django 5.1.3 on 2024-11-15 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tanushdecors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('sofa', 'Sofa'), ('chair', 'Chair'), ('table', 'Table')], max_length=10, null=True),
        ),
    ]
