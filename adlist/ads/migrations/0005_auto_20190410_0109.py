# Generated by Django 2.1.5 on 2019-04-10 01:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0004_auto_20190405_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.Ad')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ad',
            name='favorites',
            field=models.ManyToManyField(related_name='favorite_ads', through='ads.Fav', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='fav',
            unique_together={('ad', 'user')},
        ),
    ]
