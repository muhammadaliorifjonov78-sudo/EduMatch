from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("doc", "0010_verificationcode_telegram_username_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TelegramContact",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone_number", models.CharField(db_index=True, max_length=20, unique=True)),
                ("chat_id", models.BigIntegerField(unique=True)),
                ("telegram_username", models.CharField(blank=True, max_length=150)),
                ("first_name", models.CharField(blank=True, max_length=150)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name="verificationcode",
            name="phone_number",
            field=models.CharField(db_index=True, default="", max_length=20),
        ),
    ]
