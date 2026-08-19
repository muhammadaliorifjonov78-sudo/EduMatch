from django.db import migrations, models


def create_default_groups(apps, schema_editor):
    MatchingGroup = apps.get_model("doc", "MatchingGroup")

    groups = [
        {
            "title": "Frontend dasturlash",
            "academy": "Edu Academy",
            "direction": "Web Dasturlash",
            "location": "Chilonzor tumani",
            "students": 12,
            "days": ["Dushanba", "Chorshanba", "Juma"],
            "time": "18:00 - 20:00",
            "match_percent": 96,
        },
        {
            "title": "Python dasturlash",
            "academy": "IT School",
            "direction": "Dasturlash",
            "location": "Yunusobod tumani",
            "students": 8,
            "days": ["Seshanba", "Payshanba", "Shanba"],
            "time": "16:00 - 18:00",
            "match_percent": 91,
        },
        {
            "title": "Java dasturlash",
            "academy": "IT Academy",
            "direction": "Dasturlash",
            "location": "Shayxontohur tumani",
            "students": 7,
            "days": ["Dushanba", "Juma"],
            "time": "17:00 - 19:00",
            "match_percent": 84,
        },
        {
            "title": "Grafik dizayn",
            "academy": "Creative School",
            "direction": "Grafik dizayn",
            "location": "Yakkasaroy tumani",
            "students": 9,
            "days": ["Seshanba", "Payshanba"],
            "time": "18:00 - 20:00",
            "match_percent": 81,
        },
        {
            "title": "Sun'iy intellekt",
            "academy": "Future Academy",
            "direction": "Sun'iy intellekt",
            "location": "Olmazor tumani",
            "students": 6,
            "days": ["Chorshanba", "Shanba"],
            "time": "15:00 - 17:00",
            "match_percent": 78,
        },
        {
            "title": "Vue.js dasturlash",
            "academy": "Edu Academy",
            "direction": "Web Dasturlash",
            "location": "Chilonzor tumani",
            "students": 10,
            "days": ["Dushanba", "Chorshanba", "Juma"],
            "time": "16:00 - 18:00",
            "match_percent": 94,
        },
    ]

    for data in groups:
        MatchingGroup.objects.create(**data)


class Migration(migrations.Migration):

    dependencies = [
        ("doc", "0002_rename_item_cars"),
    ]

    operations = [
        migrations.CreateModel(
            name="MatchingGroup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150)),
                ("academy", models.CharField(max_length=150)),
                ("direction", models.CharField(max_length=100)),
                ("location", models.CharField(max_length=150)),
                ("students", models.PositiveIntegerField(default=0)),
                ("days", models.JSONField(default=list)),
                ("time", models.CharField(max_length=50)),
                ("match_percent", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["-match_percent", "title"]},
        ),
        migrations.RunPython(create_default_groups, migrations.RunPython.noop),
    ]
