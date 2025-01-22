# Generated by Django 5.0.6 on 2025-01-22 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='pdf_file',
            field=models.FileField(blank=True, help_text='Téléchargez un fichier PDF pour le cours.', null=True, upload_to='courses/pdfs/'),
        ),
        migrations.AddField(
            model_name='course',
            name='video_url',
            field=models.URLField(blank=True, help_text='Ajoutez un lien vers une vidéo (par exemple, YouTube).', null=True),
        ),
    ]
