# Generated by Django 4.2.3 on 2023-07-23 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_status',
            field=models.CharField(choices=[('cd', 'canceled'), ('pg', 'processing'), ('pd', 'posted')], default='i_p', max_length=2),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('like', models.IntegerField(default=0)),
                ('dislike', models.IntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
            ],
        ),
    ]