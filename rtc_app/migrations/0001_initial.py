# Generated by Django 4.2 on 2023-04-20 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('coin_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hash', models.CharField(max_length=256)),
                ('next_coin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prev_coin_reverse', to='rtc_app.coin')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('prev_coin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_coin_reverse', to='rtc_app.coin')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='GroupModel',
            fields=[
                ('group_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hash', models.CharField(max_length=256)),
                ('coin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rtc_app.coin')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatModel',
            fields=[
                ('sent_by', models.CharField(blank=True, max_length=200, null=True)),
                ('chat_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('messages', models.CharField(max_length=1000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_chats', to='rtc_app.groupmodel')),
            ],
        ),
    ]