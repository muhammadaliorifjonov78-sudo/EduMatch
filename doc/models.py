from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class TelegramContact(models.Model):
    phone_number = models.CharField(max_length=20, unique=True, db_index=True)
    chat_id = models.BigIntegerField(unique=True)
    telegram_username = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} -> {self.chat_id}"


class VerificationCode(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="verification",
    )
    code = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=20, db_index=True)
    telegram_username = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.username} - {self.code}"


class Cars(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MatchingGroup(models.Model):
    title = models.CharField(max_length=150)
    academy = models.CharField(max_length=150)
    direction = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    students = models.PositiveIntegerField(default=0)
    days = models.JSONField(default=list)
    time = models.CharField(max_length=50)
    match_percent = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-match_percent", "title"]

    def __str__(self):
        return f"{self.title} - {self.academy}"


class Course(models.Model):
    CATEGORY_CHOICES = [
        ("Dasturlash", "Dasturlash"),
        ("Web Dasturlash", "Web Dasturlash"),
        ("Grafik dizayn", "Grafik dizayn"),
        ("Mobil dasturlash", "Mobil dasturlash"),
        ("Sun'iy intellekt", "Sun'iy intellekt"),
        ("Robototexnika", "Robototexnika"),
    ]

    title = models.CharField(max_length=150)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, db_index=True)
    teacher = models.CharField(max_length=150)
    price = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0)
    students = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="courses/", blank=True)

    class Meta:
        ordering = ["-rating", "title"]

    def __str__(self):
        return self.title
