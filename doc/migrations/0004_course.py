from django.db import migrations, models


def create_courses(apps, schema_editor):
    Course = apps.get_model("doc", "Course")
    courses = [
        {"title": "Python Dasturlash", "category": "Dasturlash", "teacher": "Sardor Karimov", "price": 300000, "rating": 4.8, "students": 95, "image": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935"},
        {"title": "Java Dasturlash", "category": "Dasturlash", "teacher": "Jasur Aliyev", "price": 320000, "rating": 4.7, "students": 64, "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4"},
        {"title": "Frontend Bootcamp", "category": "Web Dasturlash", "teacher": "Ali Valiyev", "price": 350000, "rating": 4.9, "students": 120, "image": "https://images.unsplash.com/photo-1498050108023-c5249f4df085"},
        {"title": "Vue.js Dasturlash", "category": "Web Dasturlash", "teacher": "Muhammad Ali", "price": 330000, "rating": 4.9, "students": 88, "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3"},
        {"title": "Grafik Dizayn", "category": "Grafik dizayn", "teacher": "Aziza Xasanova", "price": 280000, "rating": 4.9, "students": 80, "image": "https://images.unsplash.com/photo-1561070791-2526d30994b5"},
        {"title": "Mobil Dasturlash", "category": "Mobil dasturlash", "teacher": "Javohir Ergashev", "price": 320000, "rating": 4.7, "students": 70, "image": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c"},
        {"title": "Sun'iy Intellekt Asoslari", "category": "Sun'iy intellekt", "teacher": "Dilshod Karimov", "price": 400000, "rating": 4.8, "students": 52, "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995"},
        {"title": "Robototexnika", "category": "Robototexnika", "teacher": "Bekzod Sobirov", "price": 370000, "rating": 4.6, "students": 35, "image": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e"},
    ]
    for data in courses:
        Course.objects.create(**data)


class Migration(migrations.Migration):
    dependencies = [("doc", "0003_matchinggroup")]
    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150)),
                ("category", models.CharField(max_length=100)),
                ("teacher", models.CharField(max_length=150)),
                ("price", models.PositiveIntegerField(default=0)),
                ("rating", models.FloatField(default=0)),
                ("students", models.PositiveIntegerField(default=0)),
                ("image", models.URLField(blank=True)),
            ],
            options={"ordering": ["-rating", "title"]},
        ),
        migrations.RunPython(create_courses, migrations.RunPython.noop),
    ]
