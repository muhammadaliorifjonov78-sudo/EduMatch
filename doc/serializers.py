from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Cars, Course, MatchingGroup


def normalize_phone(value):
    phone = str(value).strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if phone.startswith("00"):
        phone = "+" + phone[2:]
    if not phone.startswith("+"):
        raise serializers.ValidationError("Telefon raqamini +998901234567 ko'rinishida kiriting.")
    digits = phone[1:]
    if not digits.isdigit() or not 10 <= len(digits) <= 15:
        raise serializers.ValidationError("Telefon raqami noto'g'ri.")
    return "+" + digits


class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = "__all__"


class MatchingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingGroup
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_image(self, obj):
        if not obj.image:
            return None
        name = str(obj.image.name)
        if name.startswith(("http://", "https://")):
            return name
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_phone_number(self, value):
        return normalize_phone(value)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_phone_number(self, value):
        return normalize_phone(value)


class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField(min_length=4, max_length=4)

    def validate_phone_number(self, value):
        return normalize_phone(value)

    def validate_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Kod faqat 4 ta raqamdan iborat bo'lishi kerak.")
        return value
